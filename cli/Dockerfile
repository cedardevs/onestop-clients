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

## grap openapi file from search OS search api and build openapi go file using openapi-cli-generator
RUN go get -u github.com/danielgtaylor/openapi-cli-generator
RUN wget https://raw.githubusercontent.com/cedardevs/onestop/master/search/src/main/resources/static/openapi.yaml
RUN openapi-cli-generator generate openapi.yaml
RUN sed -i 's/package main/package generated/g' openapi.go
RUN sed -i 's/openapiRegister/OpenapiRegister/g' openapi.go
RUN mv openapi.go internal/app/generated

RUN go build ./cmd/onestop

### App
FROM scratch as cli
COPY --from=builder cli /
ENTRYPOINT ["/onestop"]