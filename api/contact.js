const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
    if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        return res.status(200).end();
    }
    
    if (req.method !== 'POST') {
        res.setHeader('Allow', 'POST');
        return res.status(405).json({ 
            ok: false, 
            error: 'Method Not Allowed' 
        });
    }
    
    try {
        const { 
            anreise, abreise, personen, kinder,
            vorname, nachname, telefon, email, nachricht 
        } = req.body;

        if (!vorname || !nachname || !email || !telefon) {
            return res.status(400).json({
                ok: false,
                error: 'Bitte füllen Sie alle Pflichtfelder aus.'
            });
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return res.status(400).json({
                ok: false,
                error: 'Bitte geben Sie eine gültige E-Mail-Adresse ein.'
            });
        }

        const transporter = nodemailer.createTransport({
            host: process.env.SMTP_HOST,
            port: Number(process.env.SMTP_PORT) || 465,
            secure: process.env.SMTP_SECURE === "true",
            auth: {
                user: process.env.SMTP_USER,
                pass: process.env.SMTP_PASS
            }
        });

        const htmlContent = `
            <h2>Neue Buchungsanfrage Lieblingsplatz Grömitz</h2>
            <table style="border-collapse:collapse;width:100%;max-width:600px;font-family:Arial,sans-serif;">
              <tr><td style="padding:10px;border-bottom:1px solid #eee;width:140px;"><b>Anreise:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${anreise || '-'}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>Abreise:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${abreise || '-'}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>Personen:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${personen || '-'}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>Kinder:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${kinder || '-'}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>Name:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${vorname} ${nachname}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>Telefon:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${telefon}</td></tr>
              <tr><td style="padding:10px;border-bottom:1px solid #eee;"><b>E-Mail:</b></td><td style="padding:10px;border-bottom:1px solid #eee;">${email}</td></tr>
              <tr><td style="padding:10px;vertical-align:top;"><b>Nachricht:</b></td><td style="padding:10px;">${(nachricht || '-').replace(/\n/g, '<br>')}</td></tr>
            </table>
        `;

        const mailOptions = {
            from: \`"Lieblingsplatz Website" <\${process.env.SMTP_USER}>\`,
            to: 'info@lieblingsplatz-groemitz.de',
            replyTo: email,
            subject: \`Neue Buchungsanfrage von \${vorname} \${nachname}\`,
            text: \`Neue Buchungsanfrage\n\nAnreise: \${anreise}\nAbreise: \${abreise}\nPersonen: \${personen}\nKinder: \${kinder}\n\nName: \${vorname} \${nachname}\nTelefon: \${telefon}\nE-Mail: \${email}\n\nNachricht:\n\${nachricht}\`,
            html: htmlContent
        };

        await transporter.sendMail(mailOptions);
        return res.status(200).json({ ok: true });
        
    } catch (error) {
        console.error('Mail-Fehler:', error);
        return res.status(500).json({
            ok: false,
            error: 'Beim Senden ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.'
        });
    }
};
