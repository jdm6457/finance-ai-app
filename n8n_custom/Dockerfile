# Start from a standard, official Debian image ("Bullseye" version)
FROM debian:bullseye-slim

# Set environment variables to non-interactively install packages
ENV DEBIAN_FRONTEND=noninteractive

# --- Install System Dependencies & Node.js (as root) ---
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    git \
    gnupg \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y --no-install-recommends nodejs

# --- Install n8n & Python Libraries (as root) ---
RUN npm install -g n8n
RUN pip install playwright

# --- User Setup & Sudo Permissions (as root) ---
# Create a non-root user 'node' for security
RUN useradd --create-home --shell /bin/bash node && \
    # Add the 'node' user to the sudo group
    usermod -aG sudo node && \
    # Give the 'node' user passwordless sudo privileges
    echo "node ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# --- Install Playwright Browsers (as the 'node' user) ---
# Switch to the 'node' user BEFORE installing browsers.
# This ensures they are installed in the correct user's directory and can use sudo.
USER node
RUN playwright install --with-deps

# --- Final Configuration ---
# Set the working directory for the application
WORKDIR /home/node

# Expose the port n8n runs on
EXPOSE 5678

# The command to run when the container starts
CMD ["n8n"]
