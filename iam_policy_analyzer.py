class IAMPolicyAnalyzer:
    @staticmethod
    def analyze_policy(policy):
        issues = []
        for statement in policy.get('Statement', []):
            # Check for wildcard actions
            if 'Action' in statement and 's3:*' in statement['Action']:
                issues.append("Wildcard permission detected: s3:*")
            # Check for overly broad resource access
            if 'Effect' in statement and statement['Effect'] == 'Allow' and '*' in statement.get('Resource', ''):
                issues.append("Overly broad resource access detected")

        return issues if issues else ["Policy is secure!"]
