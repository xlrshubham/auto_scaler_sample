docker build -t scaleit_server:latest -f Scaleit_Vimeo/Dockerfile .
docker run -it -p 8001:8123 scaleit_server:latest