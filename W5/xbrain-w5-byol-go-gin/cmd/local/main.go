// Local dev entrypoint. `go run ./cmd/local` → http://localhost:8080.
// Lambda does NOT use this file. It exists so the app stays runnable the
// "normal" way after we add Lambda support in the root main.go.
package main

import (
	"log"
	"os"

	"byol-go-gin/server"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	r := server.New()
	log.Printf("listening on http://localhost:%s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}
