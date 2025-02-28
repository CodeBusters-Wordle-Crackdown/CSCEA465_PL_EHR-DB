FROM debian:latest

# Install dependencies
RUN apt-get update && apt-get install -y g++ sqlite3 libsqlite3-dev

# Copy source code
WORKDIR /app
COPY database.cpp .

# Compile the C++ application
RUN g++ database.cpp -o database -lsqlite3

# Run the application
CMD ["./database"]
