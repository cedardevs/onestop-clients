FROM golang as builder

WORKDIR /cli

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

RUN go build ./cmd/onestop

### App
FROM scratch as cli
COPY --from=builder cli /
ENTRYPOINT ["/onestop"]