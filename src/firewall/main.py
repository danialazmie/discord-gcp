from google.cloud import compute_v1
from google.oauth2 import service_account

class FirewallManager:

    
    UNALLOWED_IPS = ['*', '0.0.0.0', '0.0.0.0/0']

    def __init__(self):
        
        self.PROJECT = "aiml-proto"
        self.FIREWALL_NAME = "e2small-allow-psql"
        self.client = compute_v1.FirewallsClient(
            credentials=service_account.Credentials.from_service_account_file("gcp-credentials.json"),
        )

    def validate_ip(self, ip: str):
        if ip in self.UNALLOWED_IPS:
            return False
        else:
            return True

    def get_firewall(self) -> bool:
        
        request = compute_v1.GetFirewallRequest(
            project=self.PROJECT,
            firewall=self.FIREWALL_NAME
        )

        response = self.client.get(request=request)

        return response
    
    def add_ip(self, ip: str) -> bool:

        is_ip_valid = self.validate_ip(ip)

        if not is_ip_valid:
            print('Invalid IP')
            return False
        
        try:

            firewall = self.get_firewall()
            firewall.source_ranges.append(ip)

            request = compute_v1.PatchFirewallRequest(
                project=self.PROJECT,
                firewall=self.FIREWALL_NAME,
                firewall_resource=firewall
            )

            self.client.patch(request=request)

            return True

        except Exception as e:
            print(e)
            return False
    
    def remove_ip(self, ip: str) -> bool:

        is_ip_valid = self.validate_ip(ip)

        if not is_ip_valid:
            print('Invalid IP')
            return False
        
        try:
            firewall = self.get_firewall()

            if ip in firewall.source_ranges:
                firewall.source_ranges.remove(ip)
            else:
                print(f'IP not found: {ip}')
                return False
            

            request = compute_v1.PatchFirewallRequest(
                project=self.PROJECT,
                firewall=self.FIREWALL_NAME,
                firewall_resource=firewall
            )

            self.client.patch(request=request)

            return True

        except Exception as e:
            print(e)
            return False
        
    def list_ips(self) -> list:

        firewall = self.get_firewall()

        return firewall.source_ranges