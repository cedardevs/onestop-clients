FROM golang:1.13-alpine AS builder

COPY . "/go/src/github.com/cedardevs/onestop-clients/cli"
WORKDIR "/go/src/github.com/cedardevs/onestop-clients/cli"
RUN apk update && apk upgrade && \
    apk add --no-cache bash git
RUN go get -u github.com/danielgtaylor/openapi-cli-generator
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build ./cmd/onestop/

CMD ["./onestop"]

#########
# second stage to obtain a very small image
FROM scratch

COPY --from=builder ./onestop .

CMD ["./onestop"]