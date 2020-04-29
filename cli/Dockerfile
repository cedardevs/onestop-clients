#FROM golang:alpine AS builder
#
#WORKDIR "/cli"
#COPY . "/go/src/github.com/cedardevs/onestop-clients/cli"
#
#RUN apk update && apk upgrade && \
#    apk add --no-cache bash git
#RUN go get -u github.com/danielgtaylor/openapi-cli-generator
##RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build .
#RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o cli /cmd/onestop/main.go
#
#CMD ["./onestop"]
#
##########
#FROM gcr.io/distroless/base@sha256:2b0a8e9a13dcc168b126778d9e947a7081b4d2ee1ee122830d835f176d0e2a70
## second stage to obtain a very small image
#FROM scratch
#
#COPY --from=builder ./onestop/onestop ./
#
#CMD ["./onestop"]

FROM golang as builder

WORKDIR /cli
COPY . "/go/src/github.com/cedardevs/onestop-clients/cli"

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# uses and caches modules so the download command
# will only be executed if something changed either on go.mod or go.sum
COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

#FROM gcr.io/distroless/base@sha256:2b0a8e9a13dcc168b126778d9e947a7081b4d2ee1ee122830d835f176d0e2a70

RUN go build ./cmd/onestop

### App
FROM scratch as cli
COPY --from=builder cli /
ENTRYPOINT ["/onestop"]