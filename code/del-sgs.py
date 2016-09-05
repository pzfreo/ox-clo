import boto3
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


for g in client.describe_security_groups(Filters=[{'Name':'group-name', 'Values':['oxclo*']}])['SecurityGroups']:
	gid = g['GroupId']
	security_group = ec2.SecurityGroup(gid)
	for p in security_group.ip_permissions:
		print p
		security_group.revoke_ingress(IpProtocol=p['IpProtocol'], FromPort=p['FromPort'], ToPort=p['ToPort'])
	security_group.delete()
