// Package server defines the Gin router as it exists today, with no Lambda
// awareness. This package can be imported by `cmd/local/main.go` (which boots
// a real HTTP server) or by `main.go` (the Lambda entrypoint).
package server

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// New builds the application router. Returns a *gin.Engine that can be
// served via http.ListenAndServe OR adapted to Lambda — same value, two
// callers.
func New() *gin.Engine {
	r := gin.New()
	r.Use(gin.Recovery())

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"ok":      true,
			"runtime": "gin",
			"message": "hello from your existing app",
		})
	})

	r.GET("/api/hello/:name", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"greeting":  "Hello, " + c.Param("name") + "!",
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
	})

	r.POST("/api/echo", func(c *gin.Context) {
		var body map[string]any
		if err := c.ShouldBindJSON(&body); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusCreated, gin.H{"echo": body})
	})

	r.NoRoute(func(c *gin.Context) {
		c.JSON(http.StatusNotFound, gin.H{"error": "not found"})
	})

	return r
}
