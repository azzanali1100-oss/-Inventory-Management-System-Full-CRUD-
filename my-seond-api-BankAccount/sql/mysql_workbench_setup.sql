CREATE DATABASE IF NOT EXISTS bank_accounts
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bank_accounts;

CREATE TABLE IF NOT EXISTS accounts (
    owner VARCHAR(255) NOT NULL PRIMARY KEY,
    balance BIGINT NOT NULL,
    CONSTRAINT check_account_balance_nonnegative CHECK (balance >= 0)
);