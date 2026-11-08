package main

import (
	"encoding/json"
	"log"
	"net/http"
	"regexp"
)

var reqBody struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func isValidEmail(email string) bool {
	emailPattern := `^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$`
	match, err := regexp.MatchString(emailPattern, email)
	if err != nil {
		return false
	}
	return match
}

func loginHandler(w http.ResponseWriter, r *http.Request) {

	var testFakeMockUsers = map[string]string{
		"user1@example.com": "password12345",
		"user2@example.com": "B7rx9OkWVdx13$QF6Imq",
		"user3@example.com": "hoxnNT4g&ER0&9Nz0pLO",
		"user4@example.com": "Log4Fun",
	}

	if r.Method == "POST" {

		decode := json.NewDecoder(r.Body)
		decode.DisallowUnknownFields()

		err := decode.Decode(&reqBody)
		if err != nil {
			http.Error(w, "Cannot decode body", http.StatusBadRequest)
			return
		}
		email := reqBody.Email
		password := reqBody.Password

		if !isValidEmail(email) {
			log.Printf("Invalid email format")
			http.Error(w, "Invalid email format", http.StatusBadRequest)
			return
		}

		storedPassword, ok := testFakeMockUsers[email]
		if !ok {
			http.Error(w, "Invalid Email or Password", http.StatusUnauthorized)
			return
		}

		if password == storedPassword {
			log.Printf("Successful login request")
			w.WriteHeader(http.StatusOK)
		} else {
			http.Error(w, "Invalid Email or Password", http.StatusUnauthorized)
		}

	} else {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
	}
}

func main() {
	http.HandleFunc("/login", loginHandler)
	log.Print("Server started. Listening on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatalf("HTTP server ListenAndServe: %q", err)
	}
}
