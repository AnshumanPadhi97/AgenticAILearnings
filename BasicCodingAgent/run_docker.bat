@echo off
setlocal
set "CONTAINER_NAME=basiccodingagentcontainer"
set "IMAGE_NAME=basiccodingagent"

echo 🔍 Checking if container "%CONTAINER_NAME%" exists...
docker inspect %CONTAINER_NAME% >nul 2>&1

if %errorlevel%==0 (
    echo ✅ Container "%CONTAINER_NAME%" exists.

    echo 🕵️ Checking if container "%CONTAINER_NAME%" is running...
    set "CONTAINER_RUNNING="
    for /f "delims=" %%R in ('docker inspect -f "{{.State.Running}}" %CONTAINER_NAME% 2^>nul') do set "CONTAINER_RUNNING=%%R"

    if /i "%CONTAINER_RUNNING%"=="true" (
        echo 🟢 Container "%CONTAINER_NAME%" is already running.
        echo 🔗 Attaching to running container...
        docker attach %CONTAINER_NAME%
    ) else (
        echo 🟡 Container "%CONTAINER_NAME%" is not running.
        echo ▶️ Starting the container...
        docker start %CONTAINER_NAME% >nul
        echo ⏳ Waiting briefly to ensure startup...
        ping -n 3 127.0.0.1 >nul
        echo 🔗 Attaching to container...
        docker attach %CONTAINER_NAME%
    )
) else (
    echo ❌ Container "%CONTAINER_NAME%" does not exist.
    echo 🛠️ Building Docker image "%IMAGE_NAME%"...
    docker build -t %IMAGE_NAME% .
    echo 🚀 Running new container "%CONTAINER_NAME%" from image "%IMAGE_NAME%"...
    docker run -it --name %CONTAINER_NAME% %IMAGE_NAME%
)

echo 🏁 Script complete!
endlocal