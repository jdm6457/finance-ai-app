# Start from a standard, official Debian image ("Bullseye" version)
# This is a stable and universally available base.
FROM debian:bullseye-slim

# Set environment variables to non-interactively install packages
ENV DEBIAN_FRONTEND=noninteractive

# --- Install System Dependencies & Node.js ---
# Switch to the root user for installation
USER root

# Install essential tools: sudo, curl, git, and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    git \
    gnupg \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js (LTS version)
# We use the official NodeSource setup script for reliability
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y --no-install-recommends nodejs

# --- Install n8n & Python Libraries ---
# Use npm (Node Package Manager) to install n8n globally
RUN npm install -g n8n

# Use pip to install the Playwright library.
# The version of pip in Debian Bullseye is older and does not require
# the --break-system-packages flag.
RUN pip install playwright

# Install the browsers (like Chrome, Firefox) that Playwright will control
# The --with-deps flag handles installing necessary system libraries
RUN playwright install --with-deps

# --- User Setup & Permissions ---
# Create a non-root user 'node' to run the application for security
RUN useradd --create-home --shell /bin/bash node && \
    # Add the 'node' user to the sudo group
    usermod -aG sudo node && \
    # Give the 'node' user passwordless sudo privileges
    echo "node ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set the working directory for the application
WORKDIR /home/node

# Change ownership of the working directory to the 'node' user
RUN chown -R node:node /home/node

# Switch to the non-root 'node' user
USER node

# --- Expose Port and Define Entrypoint ---
# Expose the port n8n runs on
EXPOSE 5678

# The command to run when the container starts
CMD ["n8n"]
