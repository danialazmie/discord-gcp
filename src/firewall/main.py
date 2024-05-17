from google.cloud import compute_v1
from google.oauth2 import service_account

class FirewallManager:

    
    UNALLOWED_IPS = ['*', '0.0.0.0', '0.0.0.0/0']
    FIREWALL_RESOURCES = {
        'service': 'e2small-allow-psql',
        'airflow': 'e2small-allow-airflow'
    }

    def __init__(self):
        self.PROJECT = "aiml-proto"
        self.client = compute_v1.FirewallsClient(
            credentials=service_account.Credentials.from_service_account_file("gcp-credentials.json"),
        )

    def is_resource_allowed(self, resource_name: str) -> bool:
        if resource_name in self.FIREWALL_RESOURCES.keys():
            return True
        else:
            return False

    def is_ip_allowed(self, ip: str) -> bool:
        if ip in self.UNALLOWED_IPS:
            return False
        else:
            return True

    def get_firewall(self, resource_name: str) -> bool:
        
        request = compute_v1.GetFirewallRequest(
            project=self.PROJECT,
            firewall=self.FIREWALL_RESOURCES[resource_name]
        )

        response = self.client.get(request=request)

        return response
    
    def add_ip(self, resource_name: str, ip: str) -> bool:

        if not self.is_ip_allowed(ip):
            print('Invalid IP')
            return False
        
        try:

            firewall = self.get_firewall(resource_name)
            firewall.source_ranges.append(ip)

            request = compute_v1.PatchFirewallRequest(
                project=self.PROJECT,
                firewall=self.FIREWALL_RESOURCES[resource_name],
                firewall_resource=firewall
            )

            self.client.patch(request=request)

            return True

        except Exception as e:
            print(e)
            return False
    
    def remove_ip(self, resource_name, ip: str) -> bool:

        if not self.is_ip_allowed(ip):
            print('Invalid IP')
            return False
        
        try:
            firewall = self.get_firewall(resource_name)

            if ip in firewall.source_ranges:
                firewall.source_ranges.remove(ip)
            else:
                print(f'IP not found: {ip}')
                return False
            

            request = compute_v1.PatchFirewallRequest(
                project=self.PROJECT,
                firewall=self.FIREWALL_RESOURCES[resource_name],
                firewall_resource=firewall
            )

            self.client.patch(request=request)

            return True

        except Exception as e:
            print(e)
            return False
        
    def list_ips(self, resource_name: str) -> list:

        firewall = self.get_firewall(resource_name)

        return firewall.source_ranges