package main

import (
	"github.com/aws/aws-lambda-go/lambda"
	"net/http"
	"os"
	"time"
)

type Response struct {
	StatusCode int    `json:"statusCode"`
	Body       string `json:"body"`
}

func Handler() (Response, error) {
	addr := os.Getenv("svc_addr")
	http.Get(addr)

	time.Sleep(1*time.Second)


	return Response{
		StatusCode: 200,
		Body:       "AWS",
	}, nil
}

func main() {
	lambda.Start(Handler)
}
