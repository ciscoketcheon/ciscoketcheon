# === Parameters ===
$from = "test@test.com"
$to = "alan@dcloud.cisco.com"
$subject = "test unsub"
$smtpServer = "esa1.dcloud.cisco.com"
$port = 25

# === Load HTML body from file and append URL ===
#$htmlBody = Get-Content -Path "C:\path\to\gray.html" -Raw
$htmlBody += "<br><br><a href='https://test.com'>https://test.com</a>"

# === Create the MailMessage ===
$mail = New-Object System.Net.Mail.MailMessage

# Add custom header first
$mail.Headers.Add("X-Advertisement", "Bulk")

# Set remaining fields
$mail.From = $from
$mail.To.Add($to)
$mail.Subject = $subject
$mail.IsBodyHtml = $true
$mail.Body = $htmlBody

# === Create SMTP Client ===
$smtp = New-Object Net.Mail.SmtpClient($smtpServer, $port)
$smtp.EnableSsl = $false  # set to $true if your server requires encryption

# === Send the email ===
$smtp.Send($mail)

Write-Host "Email sent to $to from $from"

