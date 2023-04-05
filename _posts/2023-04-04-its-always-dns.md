---
layout: post
title: "It's Always DNS - RDS Aurora Rails Connection Balancing"
description: ""
category: Technical
tags: [dns,aws,rds,aurora,ruby,rails,postgresql,load balancing]
comments: false
---
{% include JB/setup %}

![AWS Aurora CPU Usage](/images/AWS_RDS_CPU_Usage.png){: width="400" align="right" style='margin-left: 25px' }

_"Why is one of our reader instances taking all the load?"_ I asked myself one Friday afternoon at work.

The green line represents the current reader CPU usage, while the blue line represents the reader instance that automatically scaled up an hour ago.

## Checking Assumptions

![It's Not DNS, There's no way it's DNS, It was DNS](/images/itsnotdns.jpg){: width="300" align="left" style='margin-right: 25px' }

My coworker helpfully chimed in with the always useful haiku to help me focus on the important things. 

Clearly something is wrong here, I started double checking assumptions.
- AWS Aurora uses two endpoints, a reader and writer endpoint.
- The reader endpoints use round-robin load balancing via DNS.
- Our production web workers are configured to connect to the reader endpoint for read-only queries.
- Restarting our web workers appears to redistribute load evenly again and we're able to mitigate the hot-spotting when it comes up.

## So why are we seeing stickiness?

When I run `netstat -an | grep ':5432'` to see open PostgreSQL connections I see about 90% of requests stuck to one of the readers. A handful of our web workers are connected to the other readers. This seems to make sense because sometimes a web worker will timeout and automatically get restarted. This seems to force a fresh connection. We see the same behavior during a deploy or manual restart of our web workers.

We currently monkey-patch the ActiveRecord [PostgreSQLAdapter#active?](https://github.com/rails/rails/blob/bc2f390f7d2a96030532f41c08205f159e05af10/activerecord/lib/active_record/connection_adapters/postgresql_adapter.rb#L273-L280) to expire our connections periodically to help with failover events.
A naive read of it indicated that it should force a reconnection every few minutes or so and that was indeed working. Further digging discovered that it was resetting the initial PG::Connection object in the connection pool rather than reaping the connection and creating a fresh one. Lastly the [PG::Connection#reset](https://github.com/ged/ruby-pg/blob/382536b03dfea39be6d525603f5b189019ccd315/lib/pg/connection.rb#L527-L531) method doesn't force DNS to resolve again. Ooof!

## How ActiveRecord Connections Work


## What Did Work

<iframe
  src="https://carbon.now.sh/embed?bg=rgba%2874%2C144%2C226%2C1%29&t=material&wt=none&l=auto&width=680&ds=false&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=true&fl=1&fm=Fira+Code&fs=14px&lh=152%25&si=false&es=2x&wm=false&code=def%2520hello%250A%2520%2520puts%2520%2522World%2522%250Aend"
  style="width: 300px; height: 250px; border:0; transform: scale(1); overflow:hidden;"
  sandbox="allow-scripts allow-same-origin">
</iframe>


```ruby
def foo
  puts "bar"
end
```

{% highlight ruby %}
def foo
  puts 'foo'
end
{% endhighlight %}