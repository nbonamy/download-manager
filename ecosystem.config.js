module.exports = {
  apps : [{
    name: "downtobox",
    cwd: "src/",
    cmd: "src/app.py",
    interpreter: "python3",
    watch: true,
    watch_delay: 1000,
    log_date_format: "YYYY-MM-DD HH:mm:ss"
  }]
}
