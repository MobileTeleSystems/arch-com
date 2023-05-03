echo "without cache"
wrk -d 10 -t 10 -c 10 --latency -s ./get.lua http://localhost:8081/

echo "with cache"
wrk -d 10 -t 10 -c 10 --latency -s ./get.lua http://localhost:8082/