~/apache-tomcat-*/bin/shutdown.sh
cp /home/operationer/.jenkins/workspace/newkand/KandSubSystem/build/libs/KandSubSystem.jaz .
nohup python main_app.py > /dev/null 2>&1 &
