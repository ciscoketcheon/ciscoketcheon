# === Parameters ===
$from = "test@test.com"
$to = "alan@dcloud.cisco.com"
$subject = "test unsub"
$smtpServer = "esa1.dcloud.cisco.com"
$port = 25

# === Load HTML body from file ===
$htmlBody = Get-Content -Path "C:\Users\admin\Downloads\gsu-sample.html" -Raw

# === Create the MailMessage ===
$mail = New-Object System.Net.Mail.MailMessage
$mail.From = $from
$mail.To.Add($to)
$mail.Subject = $subject
$mail.IsBodyHtml = $true
$mail.Body = $htmlBody

# === Add Custom Header ===
$mail.Headers.Add("X-Advertisement", "Bulk")

# === Create SMTP Client ===
$smtp = New-Object Net.Mail.SmtpClient($smtpServer, $port)
$smtp.EnableSsl = $false  # only if your server does not require SSL
# $smtp.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials  # optional, if auth is needed

# === Send the email ===
$smtp.Send($mail)

