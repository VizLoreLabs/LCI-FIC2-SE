#!/bin/sh
HOST=$1
PORT=$2
[ "$HOST" ] || HOST="localhost"
[ "$PORT" ] || PORT="4545"
echo "Entering FIC2Lab smoke test sequence. LCI's validation procedure of SE Context Aware Recommendation (Recommendation Matrix PreparationModul) engaged. Target host: $HOST:$PORT"
echo "Waiting for initialization of the docker image"
retry=0
while [ $retry -lt 14 ]; do
nc -z $HOST $PORT
if [ "$?" -eq "0" ] ; then
echo "Docker image initialized";	
break;
fi
echo -n ".";	
retry=$(($retry+1));
sleep $retry;
done
if [ $retry -eq 14 ]; then
echo "Docker not initialized. Aborting test sequence.";
exit 1;
fi
echo "Run smoke test for getting the recommendation for some users"
ITEM_RESULT2=`curl -s -o /dev/null -w '%{http_code}' "http://$HOST:$PORT/recommend/?uuid=19&lat=41.402486&lon=2.188002&ts=19999"`
if [ $ITEM_RESULT2 -ne "200" ]; then
echo "Curl command for getting the recommendation for some users failed. Validation procedure terminated."
echo "Debugging information: HTTP code $ITEM_RESULT2 instead of 200 expected from $HOST"
exit 1;
else
echo "Curl command for getting the recommendation for some users OK."
fi
echo "Smoke test completed. LCI component validation procedure succeeded. Over."
exit 0;
