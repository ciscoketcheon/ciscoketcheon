
const express = require('express')
const multer = require('multer')
const nodemailer = require('nodemailer')

const app = express()
const upload = multer()

app.post('/api/parse', upload.any(), async (req, res) => {

        const body = req.body

            console.log("dkim: ", body.dkim);
            console.log("to: ", body.to);
            console.log("cc: ", body.cc);
            console.log("from: ", body.from);
            console.log("subject: ", body.subject);
            console.log("sender_ip: ", body.sender_ip);
            console.log("spam_report: ", body.spam_report);
            console.log("envelope: ", body.envelope);
            console.log("charsets: ", body.charsets);
            console.log("SPF: ", body.SPF);
            console.log("spam_score: ", body.spam_score);


            if (req.files.length > 0) {
                // Log file data
                console.log(req.files)
            } else {
                console.log('No files...')
            }

            // Create a nodemailer transport object for sending email
            const transporter = nodemailer.createTransport({
                host: 'esa15.sgcweb.org',
                port: 25,
                secure: false
            })

            const message = {
                from: body.from,
                to: body.to,
                subject: body.subject,
                text: 'See attachment for message content',
                attachments: req.files
            }

            // Send the email
            transporter.sendMail(message, (error, info) => {
                if (error) {
                    console.log('Error sending email:', error)
                    res.status(500).send('Error sending email')
                } else {
                    console.log('Email sent:', info.response)
                    res.status(200).send('Email forwarded successfully')
                }
            })
})
        //    return res.status(200).send()
        // })

app.listen(3000, () => {
    console.log('Webserver running on -> http://localhost:3000')
})

