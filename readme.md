#  1. Run the cluster :

``` 
sudo docker compose up -d
```

#  2. Publish an example task the the cluster 



```
docker compose exec ray-client python /app/task.py

```