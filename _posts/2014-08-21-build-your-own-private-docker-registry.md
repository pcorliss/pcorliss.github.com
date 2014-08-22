---
layout: post
title: "Build Your Own Private Docker Registry for $3/month"
date: 2014-08-21
comments: false
---

We recently needed to deploy and start hosting a new venture I'm working on, [GitSentry](https://gitsentry.com). Because of a fairly complicated setup on our part [Heroku](https://www.heroku.com/) was out of the question. I had been working with [Docker](https://www.docker.com/) prior to this so it seemed like the logical next step for service configuration and deployment. One problem, I needed the host my docker images in a registry, but I didn't want my code to be public. A number of [private docker registries](#private-docker-registry-services) have popped up recently, but I'm not always rational when it comes to valuing my time against small monthly fees. So I went down the path of investigating what it would take to host my own registry.

[docker/docker-registry](https://github.com/docker/docker-registry)
----------------------

This will be easy! There's already a private registry docker image available and built for this purpose. But a few problems, we need to host it, configure the host, configure persistent storage, and configure secure access.

Hosting
-------

Finding a persistent online host isn't easy. [DigitalOcean](https://www.digitalocean.com/?refcode=e1808aec974e) is the cheapest at $5/mo. AWS is competitive at about $9/mo or $0.013/hr for their t2.micro instances. But you can get a little bit better by paying some money upfront for a 3 year reserved instance averaging out to $4.50/mo. But even better than that you can leverage spot instances at $0.0031/hr or about $3/mo after some additional support fees (EBS and transfer).

Spot Instances
--------------

Normally reserved for a different type of workload you can leverage a spot request by setting your maximum bid high enough to get almost persistence. You might still be out-bid or the instance might fail due to a service interruption. Fortunately you can use cloud-config on the Amazon Linux AMIs to automatically start the registry on boot, and S3 for storage.

S3 Configuration
----------------

You'll need to store the docker images somewhere. The docker registry provides several possible endpoints but s3 is the most convenient. Create a bucket in s3 and note the name.

For security purposes I like to provision a custom user with access to only that bucket and nothing else. This is the custom IAM policy I use. Note the access key and secret after creating the user.

```
{
  "Version": "2012-10-17",
  "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::your-bucket",
                "arn:aws:s3:::your-bucket/*"
            ]
        }
  ]
}
```

DynDNS
------

I use [Namecheap](http://www.namecheap.com/?aff=72667) as my registrar and DNS provider for non-critical domains. They also provide a handy DynDNS service that allows me to curl a url and set the ip address for a hostname. Any other DynDNS service should be able to do the job if you don't use Namecheap.

My spot instance has been running for about 70 days now without interruption so you might be able to get away with doing this manually to avoid extra setup.

EC2 Configuration
-----------------

### Select an Availability Zone
Each AWS account has a different mapping for availability zones. This prevents me from suggesting the zone which has the least amount of price variance for spot instances. Under ```EC2 -> Spot Requests -> Pricing History``` you can view the volatility under different zones for t1.micro instances over the last 3 months. Pick the one that stays nearest to the baseline.

### Define a Security Group

I define a custom security group for my docker registry which exposes HTTP and SSH to just my IP address. You may want to do the same otherwise your private registry will be world readable and writeable. There's an [authentication section](https://github.com/docker/docker-registry/#authentication-options) available with more info on limiting access.

### Spot Instance Configuration

* Select the latest Amazon Linux AMI with paravirtual support. At the time this was written that was ```Amazon Linux AMI 2014.03.2 (PV) - ami-7c807d14```.
* Select the t1.micro instance type
* Specify your maximum bid. The higher this is the more likely your instance will stay persistent but may result in a higher monthly cost. I set mine to $0.0075/hr but have rarely seen my costs rise above the baseline of $0.0031/hr.
* Turn on Persistent request. This will request new spot instances if you get out bid or an instance dies for some reason.
* Select the Availability Zone you determined from the pricing history.
* Advanced -> User Data: This is run after boot on your instance. Make sure to replace the values in brackets with your own values. 

```
#cloud-config
runcmd:
 - "echo 'Running Docker Setup and Registry'"
 - 'IPADDR=$(curl http://169.254.169.254/latest/meta-data/public-ipv4) && curl -i "https://dynamicdns.park-your-domain.com/update?host=[hostname]&domain=[domain]&password=[password]&ip=$IPADDR"'
 - "yum update -y"
 - "yum install docker -y"
 - "/etc/init.d/docker start"
 - "docker run -d -e SETTINGS_FLAVOR=s3 -e AWS_BUCKET=[YOUR_S3_BUCKET] -e STORAGE_PATH=/registry -e AWS_KEY=[YOUR_AWS_KEY] -e AWS_SECRET=[YOUR_AWS_SECRET] -e SEARCH_BACKEND=sqlalchemy -e STORAGE_REDIRECT=true -p '80:5000' registry"
 - "echo 'Done Setting up Docker'"
```

* Select a Security Group from the list as defined earlier.

Startup is much slower than normal on-demand instances so make sure to budget about 15-20 minutes for the instance request, boot, package installation, and docker image download.

Testing 1, 2, 3
---------------
If all went well you should see something like the following when you curl your endpoint. "docker-registry server (s3) (v0.8.0)"

Run the following commands for a full end-to-end test

```
docker pull ubuntu:latest
docker tag ubuntu:latest [endpoint_fqdn]/ubuntu_test
docker push [endpoint_fqdn]/ubuntu_test
docker pull [endpoint_fqdn]/ubuntu_test
```

Private Docker Registry Services
--------------------------------

* [Docker Hub](https://registry.hub.docker.com/plans/) - $7-$12/mo
* [Quay.io](https://quay.io/plans/) - $12-25/mo
* [Tutum](https://www.tutum.co/pricing/) - $4/mo

### Full Disclosure
* The [Namecheap](http://www.namecheap.com/?aff=72667) and [DigitalOcean](https://www.digitalocean.com/?refcode=e1808aec974e) links use my referral code.
