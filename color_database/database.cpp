#include <iostream>
#include <sqlite3.h>

void getUserInput(std::string &username, std::string &password, std::string &color) {
    std::cout << "Enter username: ";
    std::getline(std::cin, username);
    
    std::cout << "Enter password: ";
    std::getline(std::cin, password);
    
    std::cout << "Enter favorite color: ";
    std::getline(std::cin, color);
}

int createDatabase() {
    sqlite3* DB;
    int exit = sqlite3_open("users.db", &DB);
    
    if (exit) {
        std::cerr << "Error opening database: " << sqlite3_errmsg(DB) << std::endl;
        return exit;
    }
    
    std::string sql = "CREATE TABLE IF NOT EXISTS users ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "username TEXT NOT NULL, "
                      "password TEXT NOT NULL, "
                      "favorite_color TEXT NOT NULL);";
    
    char* errorMessage;
    exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &errorMessage);
    
    if (exit != SQLITE_OK) {
        std::cerr << "Error creating table: " << errorMessage << std::endl;
        sqlite3_free(errorMessage);
    } else {
        std::cout << "Table created successfully!" << std::endl;
    }
    
    sqlite3_close(DB);
    return 0;
}

int insertUser(const std::string& username, const std::string& password, const std::string& color) {
    sqlite3* DB;
    sqlite3_open("users.db", &DB);
    
    std::string sql = "INSERT INTO users (username, password, favorite_color) VALUES ('" + username + "', '" + password + "', '" + color + "');";
    
    char* errorMessage;
    int exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &errorMessage);
    
    if (exit != SQLITE_OK) {
        std::cerr << "Error inserting data: " << errorMessage << std::endl;
        sqlite3_free(errorMessage);
    } else {
        std::cout << "User added successfully!" << std::endl;
    }
    
    sqlite3_close(DB);
    return 0;
}

int main() {
    createDatabase();
    
    std::string username, password, color;
    getUserInput(username, password, color);
    
    insertUser(username, password, color);
    
    return 0;
}
