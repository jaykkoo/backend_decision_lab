# ===============================
# Builder
# ===============================
FROM rust:bookworm AS builder

WORKDIR /app

COPY rust-toolchain.toml ./
COPY Cargo.toml Cargo.lock ./

# Cache deps
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src
RUN rm -f target/release/rust_engine

# Real source
COPY src ./src
RUN cargo build --release

# ===============================
# Runtime (distroless)
# ===============================
FROM gcr.io/distroless/cc-debian12

WORKDIR /app

COPY --from=builder /app/target/release/rust_engine /app/rust_engine

# Distroless = pas de chmod possible ici → OK car binaire déjà exécutable

ENV MODE=worker

USER nonroot:nonroot

ENTRYPOINT ["/app/rust_engine"]
