git pull
mvn clean package
APP_NAME=ask_portal-1.0-SNAPSHOT.jar
echo $APP_NAME
tokill=`ps -ef | grep java | grep $APP_NAME | awk '{print $2}'`
kill -9 $tokill
echo $tokill
echo 'kill success'
rm -rf /analy/analysis/api/ask_portal-1.0-SNAPSHOT.jar
rm -rf /analy/analysis/api/resources
rm -rf /analy/analysis/api/lib
cp -R target/ask_portal-1.0-SNAPSHOT.jar /analy/analysis/api/
cp -R target/lib /analy/analysis/api/
cp -R target/resources /analy/analysis/api/
cd /analy/analysis/api
nohup java -jar /analy/analysis/api/ask_portal-1.0-SNAPSHOT.jar > /analy/analysis/api/log.file 2>&1 &
