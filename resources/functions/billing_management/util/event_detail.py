from collections import UserDict

class EventDetail(UserDict):
    def safe_get(self, key, default=None):
        if key not in self:
            print(f"Warning: Key {key} not found in event detail, using default value '{default}'")
        return super().get(key, default)

    def get(self, key, default=None):
        if key not in self:
            raise KeyError(f"Error: Required key {key} not found in event detail")
        return super().get(key, default)

    def safe_get_nested(self, key, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            new_value = value.get(k, default)
            if new_value:
                value = new_value
            else:
                print(f"Warning: Key {key} not found in event detail, using default value '{default}'")
                return default
        return value
    
    def get_email(self):
        return self.safe_get('email', f'{self.get('tenantId')}@example.com')