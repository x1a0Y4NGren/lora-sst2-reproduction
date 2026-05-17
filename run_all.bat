@echo off
setlocal

set BATCH_SIZE=%1
if "%BATCH_SIZE%"=="" set BATCH_SIZE=8

powershell -ExecutionPolicy Bypass -File "%~dp0run_all.ps1" -BatchSize %BATCH_SIZE%
