# from msilib.schema import MIME
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sqlite3 import IntegrityError
from dotenv import load_dotenv
from random import randint
from ..responses.responses import bad_request, http_ok
from ..views import requests

# retrive sender email credentials
load_dotenv()
EMAIL_NOTREPLY = os.getenv('EMAIL_NOTREPLY')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_mail_for_registration_confirmation(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize'):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Login to your Scoretize here account&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Hi """ +str(name[0].upper())+str(name[1:])+ """!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       Welcome to Scoretize
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 25px; padding-left: 0px; padding-right: 0px; padding-top: 25px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/welcome.png?raw=true" width="260" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       You're all set now, let's get started!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(os.environ["APP_URL"])+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">LOG IN TO MY NEW ACCOUNT</span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Welcome to the simplest and <strong>most efficient</strong> way of getting all the <strong>diagnostics you need</strong> to discover opportunities and gain <strong>insights on competitors.</strong>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Any doubts?
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Feel free to send us a message in our live chat on the website, or email us at <a style="color: inherit !important;" href="mailto: support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f" 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Login to your Scoretize here account&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  
                  
                  
               </tr>
            </table>
      </tr>
      <tr>
         
      </tr>
      <tr>
         
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>
        """
        
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY, EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)
# MAIL TO SEND RESET LINK

def send_mail_for_project_confirmation(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['alejandra.elsin@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize'):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE STYLES*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Check out your new project in Scoretize here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Hi """ +str(name[0].capitalize())+ """!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       New Project Available
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 25px; padding-left: 0px; padding-right: 0px; padding-top: 25px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/new-project.png?raw=true" width="260" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Now that we’re ready, let’s get going!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(os.environ["APP_URL"])+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">CHECK MY NEW PROJECT</span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Your fastest solution to measure your digital efficiency score across various digital channels against category and industry competitors.
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Don’t hesitate to contact us
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Need any help? Please, send us a message in our live chat on the website, or email us at <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                             </td>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>"""

        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY,EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)

def link_active(email):
   base_url = os.environ["BASE_URL"]
   url_user_activation = base_url + "/user/register/active-profile/"
   temp = {}
   temp["email"] = email
   requests.post(url_user_activation, json=temp)
   return True

def send_mail_for_email_verification( text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize', link=''):
    try:
        base_url = os.environ["BASE_URL"]
        url_user_activation = base_url + "/user/register/active-profile/?email="
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Confirm your email to finish your registration here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Hi """ +str(name.capitalize())+ """!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       Welcome to Scoretize
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 25px; padding-left: 0px; padding-right: 0px; padding-top: 25px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/registration_confirm_email.png?raw=true" width="260" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Before we start we’ll need to confirm your email
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(url_user_activation)+str(to_emails[0])+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">CONFIRM YOUR EMAIL</span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Welcome to the simplest and <strong>most efficient</strong> way of getting all the <strong>diagnostics you need</strong> to discover opportunities and gain <strong>insights on competitors.</strong>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Any doubts?
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Feel free to send us a message in our live chat on the website, or email us at <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                             </td>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>"""
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY, EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)

    finally:
        server.quit()
    return http_ok('Successful request')


# MAIL TO SEND TOKEN
def send_mail_for_reset_token( text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize'):
    try:
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        reset_token = random_with_N_digits(6)
        html = """ <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
  <title>Responsive HTML Email Template</title>
  <style type="text/css">
    /* reset */
    article,
    aside,
    details,
    figcaption,
    figure,
    footer,
    header,
    hgroup,
    nav,
    section,
    summary {
      display: block
    }
    audio,
    canvas,
    video {
      display: inline-block;
      *display: inline;
      *zoom: 1
    }
    audio:not([controls]) {
      display: none;
      height: 0
    }
    [hidden] {
      display: none
    }
    html {
      font-size: 100%;
      -webkit-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%
    }
    html,
    button,
    input,
    select,
    textarea {
      font-family: sans-serif
    }
    body {
      margin: 0;
      font-family: 'Source Sans Pro', sans-serif;
    }
    a:focus {
      outline: thin dotted
    }
    a:active,
    a:hover {
      outline: 0
    }
    h1 {
      font-size: 2em;
      margin: 0 0.67em 0;
    }
    h2 {
      font-size: 1.5em;
      margin: 0 0 .83em 0
    }
    h3 {
      font-size: 1.17em;
      margin: 1em 0
    }
    h4 {
      font-size: 1em;
      margin: 1.33em 0
    }
    h5 {
      font-size: .83em;
      margin: 1.67em 0
    }
    h6 {
      font-size: .75em;
      margin: 2.33em 0
    }
    abbr[title] {
      border-bottom: 1px dotted
    }
    b,
    strong {
      font-weight: bold
    }
    blockquote {
      margin: 1em 40px
    }
    dfn {
      font-style: italic
    }
    mark {
      background: #ff0;
      color: #000
    }
    p,
    pre {
      margin: 1em 0
    }
    code,
    kbd,
    pre,
    samp {
      font-family: monospace, serif;
      _font-family: 'courier new', monospace;
      font-size: 1em
    }
    pre {
      white-space: pre;
      white-space: pre-wrap;
      word-wrap: break-word
    }
    q {
      quotes: none
    }
    q:before,
    q:after {
      content: '';
      content: none
    }
    small {
      font-size: 75%
    }
    sub,
    sup {
      font-size: 75%;
      line-height: 0;
      position: relative;
      vertical-align: baseline
    }
    sup {
      top: -0.5em
    }
    sub {
      bottom: -0.25em
    }
    dl,
    menu,
    ol,
    ul {
      margin: 1em 0
    }
    dd {
      margin: 0 0 0 40px
    }
    menu,
    ol,
    ul {
      padding: 0 0 0 40px
    }
    nav ul,
    nav ol {
      list-style: none;
      list-style-image: none
    }
    img {
      border: 0;
      -ms-interpolation-mode: bicubic
    }
    svg:not(:root) {
      overflow: hidden
    }
    figure {
      margin: 0
    }
    form {
      margin: 0
    }
    fieldset {
      border: 1px solid #c0c0c0;
      margin: 0 2px;
      padding: .35em .625em .75em
    }
    legend {
      border: 0;
      padding: 0;
      white-space: normal;
      *margin-left: -7px
    }
    button,
    input,
    select,
    textarea {
      font-size: 100%;
      margin: 0;
      vertical-align: baseline;
      *vertical-align: middle
    }
    button,
    input {
      line-height: normal
    }
    button,
    html input[type="button"],
    input[type="reset"],
    input[type="submit"] {
      -webkit-appearance: button;
      cursor: pointer;
      *overflow: visible
    }
    button[disabled],
    input[disabled] {
      cursor: default
    }
    input[type="checkbox"],
    input[type="radio"] {
      box-sizing: border-box;
      padding: 0;
      *height: 13px;
      *width: 13px
    }
    input[type="search"] {
      -webkit-appearance: textfield;
      -moz-box-sizing: content-box;
      -webkit-box-sizing: content-box;
      box-sizing: content-box
    }
    input[type="search"]::-webkit-search-cancel-button,
    input[type="search"]::-webkit-search-decoration {
      -webkit-appearance: none
    }
    button::-moz-focus-inner,
    input::-moz-focus-inner {
      border: 0;
      padding: 0
    }
    textarea {
      overflow: auto;
      vertical-align: top
    }
    table {
      border-collapse: collapse;
      border-spacing: 0
    }
    /* custom client-specific styles including styles for different online clients */
    .ReadMsgBody {
      width: 100%;
    }
    .ExternalClass {
      width: 100%;
    }
    /* hotmail / outlook.com */
    .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {
      line-height: 100%;
    }
    /* hotmail / outlook.com */
    table,
    td {
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
    }
    /* Outlook */
    #outlook a {
      padding: 0;
    }
    /* Outlook */
    img {
      -ms-interpolation-mode: bicubic;
      display: block;
      outline: none;
      text-decoration: none;
    }
    /* IExplorer */
    body,
    table,
    td,
    a,
    li,
    blockquote {
      -ms-text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
      font-weight: normal !important;
    }
    .ExternalClass td[class="ecxflexibleContainerBox"] h3 {
      padding-top: 10px !important;
    }
    /* hotmail */
    /* email template styles */
    h1 {
      display: block;
      font-size: 26px;
      font-style: normal;
      font-weight: normal;
      line-height: 100%;
    }
    h2 {
      display: block;
      font-size: 20px;
      font-style: normal;
      font-weight: normal;
      line-height: 120%;
    }
    h3 {
      display: block;
      font-size: 17px;
      font-style: normal;
      font-weight: normal;
      line-height: 110%;
    }
    h4 {
      display: block;
      font-size: 18px;
      font-style: italic;
      font-weight: normal;
      line-height: 100%;
    }
    .flexibleImage {
      height: auto;
    }
    table[class=flexibleContainerCellDivider] {
      padding-bottom: 0 !important;
      padding-top: 0 !important;
    }
    body,
    #bodyTbl {
      background-color: #E1E1E1;
    }
    #emailHeader {
      background-color: #E1E1E1;
    }
    #emailBody {
      background-color: #FFFFFF;
    }
    #emailFooter {
      background-color: #E1E1E1;
    }
    .textContent {
      color: #8B8B8B;
      font-family: Helvetica;
      font-size: 16px;
      line-height: 125%;
      text-align: Left;
    }
    .textContent a {
      color: #205478;
      text-decoration: underline;
    }
    .emailButton {
      background-color: #205478;
      border-collapse: separate;
    }
    .buttonContent {
      color: #FFFFFF;
      font-family: Helvetica;
      font-size: 18px;
      font-weight: bold;
      line-height: 100%;
      padding: 15px;
      text-align: center;
    }
    .buttonContent a {
      color: #FFFFFF;
      display: block;
      text-decoration: none !important;
      border: 0 !important;
    }
    #invisibleIntroduction {
      display: none;
      display: none !important;
    }
    /* hide the introduction text */
    /* other framework hacks and overrides */
    span[class=ios-color-hack] a {
      color: #275100 !important;
      text-decoration: none !important;
    }
    /* Remove all link colors in IOS (below are duplicates based on the color preference) */
    span[class=ios-color-hack2] a {
      color: #205478 !important;
      text-decoration: none !important;
    }
    span[class=ios-color-hack3] a {
      color: #8B8B8B !important;
      text-decoration: none !important;
    }
    /* phones and sms */
    .a[href^="tel"],
    a[href^="sms"] {
      text-decoration: none !important;
      color: #606060 !important;
      pointer-events: none !important;
      cursor: default !important;
    }
    .mobile_link a[href^="tel"],
    .mobile_link a[href^="sms"] {
      text-decoration: none !important;
      color: #606060 !important;
      pointer-events: auto !important;
      cursor: default !important;
    }
    /* Cards */
    .card {
      box-shadow: 0px 8px 16px #7A7EDB69 !important;
      border-radius: 20px !important;
      margin: 0 auto;
      padding: 2rem 1rem;
      box-sizing: border-box;
    }
    .btn-primary {
      background-color: #5858D6;
      padding: 20px;
      margin: 1.5rem 0;
      border-radius: 15px;
      font-weight: bold;
      font-size: 30px;
    }
    .copyright-text {
      text-align: center;
      font-size: 14px;
      letter-spacing: 0px;
      color: #354052;
      font-weight: 300;
    }
    /* responsive styles */
    @media only screen and (max-width: 480px) {
      body {
        width: 100% !important;
        min-width: 100% !important;
      }
      table[id="emailHeader"],
      table[id="emailBody"],
      table[id="emailFooter"],
      table[class="flexibleContainer"] {
        width: 100% !important;
      }
      td[class="flexibleContainerBox"],
      td[class="flexibleContainerBox"] table {
        display: block;
        width: 100%;
        text-align: left;
      }
      td[class="imageContent"] img {
        height: auto !important;
        width: 100% !important;
        max-width: 100% !important;
      }
      img[class="flexibleImage"] {
        height: auto !important;
        width: 100% !important;
        max-width: 100% !important;
      }
      img[class="flexibleImageSmall"] {
        height: auto !important;
        width: auto !important;
      }
      table[class="flexibleContainerBoxNext"] {
        padding-top: 10px !important;
      }
      table[class="emailButton"] {
        width: 100% !important;
      }
      td[class="buttonContent"] {
        padding: 0 !important;
      }
      td[class="buttonContent"] a {
        padding: 15px !important;
      }
    }
  </style>
  <!--
      MS Outlook custom styles
    -->
  <!--[if mso 12]>
      <style type="text/css">
        .flexibleContainer{display:block !important; width:100% !important;}
      </style>
    <![endif]-->
  <!--[if mso 14]>
      <style type="text/css">
        .flexibleContainer{display:block !important; width:100% !important;}
      </style>
    <![endif]-->
</head>
<body bgcolor="#E1E1E1" leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
  <center style="background-color:#E1E1E1;">
    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTbl" style="table-layout: fixed;max-width:100% !important;width: 100% !important;min-width: 100% !important;">
      <tr>
        <td align="center" valign="top" id="bodyCell">
          <table bgcolor="#E1E1E1" border="0" cellpadding="0" cellspacing="0" width="500" id="emailHeader">
            <tr>
              <td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="10" cellspacing="0" width="500" class="flexibleContainer">
                        <tr>
                          <td valign="top" width="500" class="flexibleContainerCell">
                            <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%">
                              <tr>
                                <td align="left" valign="middle" id="invisibleIntroduction" class="flexibleContainerBox" style="display:none;display:none !important;">
                                  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:100%;">
                                    <tr>
                                      <td align="left" class="textContent">
                                        <div style="font-size:13px;color:#828282;text-align:center;line-height:120%; font-weight: 700;">
                                          Forgot your password?
                                        </div>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                                <td align="right" valign="middle" class="flexibleContainerBox">
                                  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:100%;">
                                    <tr>
                                      <td align="left" class="textContent">
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" width="500" id="emailBody">
            <tr>
              <td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color:#20234E;">
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                        <tr>
                          <td align="center" valign="top" width="500" class="flexibleContainerCell">
                            <table border="0" cellpadding="5" cellspacing="0" width="100%">
                              <tr>
                                <td align="center" valign="top" class="textContent" style="background-color:white;"> <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" alt='Scoretize icon' style="
width: 35%;" /></td>
                              </tr>
                            </table>
                            <table border="0" cellpadding="30" cellspacing="0" width="100%">
                        </tr>
                        <tr>
                          <td align="center" valign="top" class="textContent">
                            <div class="textContent card">
                              <h2 style="text-align:center;font-weight:normal;font-family:Helvetica,Arial,sans-serif;font-size:23px;margin-bottom:10px;color:#20234E;line-height:135%;">Hi Shri</h2>
                              <h1 style="color:#FFFFFF;line-height:100%;font-size:32px;font-weight:600;margin:.75rem 0;text-align:center; color:#20234E;">Forgot your password?</h1>
                 <h2 style="text-align:center;font-weight:normal;font-family:Helvetica,Arial,sans-serif;font-size:23px;margin-bottom:10px;color:#20234E;line-height:135%;">It happens to all of us! We got you!</h2>             
                              
                              <img style="margin: 2rem auto; width: 60%;" src='https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/query.png?raw=true' alt='Welcome image' />
                              <h2 style="text-align:center;font-weight:normal;font-family:Helvetica,Arial,sans-serif;font-size:20px;margin-bottom:10px;color:#20234E;line-height:135%;">To reset your password, click on the bottom bellow:</h2>
                              <div class="btn-primary" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:15px;margin-bottom:0;color:#FFFFFF;line-height:135%;">RESET MY PASSWORD</div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td>
                            
                            <div class="card" style="margin-bottom: 3em;">
                              <h2 style="text-align:center;font-weight:500;font-family:Helvetica,Arial,sans-serif;font-size:32px;margin-bottom:10px;color:#20234E;line-height:135%;">We’re here to help!</h2>
                              <p style="text-align:center;font-weight:300;font-family:Helvetica,Arial,sans-serif;font-size:23px;margin-bottom:10px;color:#20234E;line-height:135%;"> Feel free to send us a message in our live chat on the website, or email us at <span style="text-decoration: underline">support@scoretize.com</span></p>
                            </div>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td align="center" valign="top">
          <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                  <tr>
                    <td align="center" valign="top" width="500" class="flexibleContainerCell">
                    </td>
                  </tr>
                  <!-- divider -->
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#EFEFEF">
                        <tr>
                          <td align="center" valign="top">
                            <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                              <tr>
                                <td align="center" valign="top" width="500" class="flexibleContainerCell">
                                  <table border="0" cellpadding="30" cellspacing="0" width="100%">
                                    <tr>
                                      <td align="center" valign="top">
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom:20px;">
                                          <tr>
                                            <td valign="top" class="textContent">
                                              <div style="width: 80%; margin:0 auto;">
                                                <h1 style="color:#FFFFFF;line-height:100%;font-family:Helvetica,Arial,sans-serif;font-size:35px;font-weight:normal;margin-bottom:5px;text-align:center; color:#20234E; font-weight:700;">Follow us to stay updated</h1>
                                                <p style="text-align:center;font-weight:200;font-family:Helvetica,Arial,sans-serif;font-size:18px;margin-bottom:10px;color:#20234E;line-height:135%; font-weight: 300;"> Help us improve by sharing your feedback in this short <a href="https://thekeenfolks.typeform.com/scoretize" style="color: inherit;">survey</a></p>
                                            </td>
                                          </tr>
                                        </table>
                                        <table border="0" cellpadding="0" cellspacing="0" width="50%" style="background-color: #3498DB;">
                                          <tr>
                                            <img src="https://raw.githubusercontent.com/TheKeenfolksDigital/Scoretize_resources/dev/email_resources/images/social_media_icon.png" style="
width: 35%; margin: 2rem 0" />
                                            <p class="copyright-text">Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.</p>
                                            <p class="copyright-text" style="font-weight: 400;"> support@scoretize.com | +34 605 351 325</p>
                                            </div>
                                          </tr>
                                        </table>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                          <td align="center" valign="top">
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
              </td>
            </tr>
          </table>
  </center>
</body>
</html>
      """
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY, EMAIL_PASS)
        server.sendmail(from_email, to_emails, msg_str)
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)

    finally:
        server.quit()
    return reset_token


def send_mail_for_password_reset_succesful(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support'):
    try:
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)
        reset_token = random_with_N_digits(6)
        html_part = MIMEText(f"<p>Your password has been set successfully</p>")
        msg.attach(html_part)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY, EMAIL_PASS)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)

    finally:
        server.quit()


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_mail_for_project_fail(reset_token=None, text='Email_body', subject='Automated reply for failed project', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize'):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <!--Help character display properly.-->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <!--Set the initial scale of the email.-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <!--Force Outlook clients to render with a better MS engine.-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge">
  <!--Help prevent blue links and autolinking-->
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
  <!--prevent Apple from reformatting and zooming messages.-->
  <meta name="x-apple-disable-message-reformatting">
  <!--target dark mode-->
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark only">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
  <title>Scoretize</title>
  <style type="text/css">
     body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
     #outlook a {
     padding: 0;
     }
     body {
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     background: white;
     width: 100% !important;
     -webkit-text-size-adjust: 100%;
     -ms-text-size-adjust: 100%;
     margin-top: 0px;
     margin-right: 0px;
     margin-bottom: 0px;
     margin-left: 0px;
     padding-top: 0px;
     padding-right: 0px;
     padding-bottom: 0px;
     padding-left: 0px;
     }
     .ExternalClass {
     width: 100%;
     }
     .ExternalClass * {
     line-height: 100%;
     }
     .ExternalClass,
     .ExternalClass p,
     .ExternalClass span,
     .ExternalClass font,
     .ExternalClass td,
     .ExternalClass div {
     line-height: 100%;
     }
     img {
     outline: none;
     text-decoration: none;
     -ms-interpolation-mode: bicubic;
     }
     a img {
     border: none;
     }
     .image-fix {
     display: block;
     }
     /*TYPOGRAPHY */
     .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
     .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
     .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
     .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
     .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
     .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
     .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
     .unsub-text {
     mso-line-height-rule: exactly;
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     font-size: 15px;
     line-height: 15px;
     font-weight: normal;
     text-decoration: none;
     color: #cbd0d6;
     }
     .unsub-text a {
     text-decoration: none;
     color: #cbd0d6;
     }
     .address-text {
     mso-line-height-rule: exactly;
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     font-size: 15px;
     line-height: 15px;
     font-weight: normal;
     text-decoration: none;
     color: #cbd0d6;
     }
     .address-text a {
     text-decoration: none;
     color: #cbd0d6;
     }
     .emailButton{
     box-sizing: border-box;
     max-width:600px !important;
     width:100% !important;
     }
     .footer-sm {                  box-sizing: border-box;
     max-width:600px !important;
     width:100% !important;}
  </style>
  <!--mobile styles-->
  <style>
     @media screen and (max-width:600px) {
     .wFull { width: 100% !important; }
     .imgFull { width: 70% !important; height: auto !important; }
     .h1 {font-size: 26px !important; line-height: 36px !important;}
     .h2 {font-size: 24px !important; line-height: 32px !important;}
     .text-base {font-size: 20px !important; line-height: 28px !important;}
     .text-sm {font-size: 14px !important; line-height: 20px !important;}
     .text-xs {font-size: 12px !important; line-height: 16px !important;}
     .text-xxs {font-size: 11px !important; line-height: 16px !important;}
     .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
     .emailButton{
     max-width:100% !important;
     width:100% !important;
     }
     .emailButtonContent {
     padding-right: 10px !important;
     padding-left: 10px !important;
     }
     .emailButton a{
     display:block !important;
     font-size:17px !important;
     }
     }
     /*DARK MODE*/
     @media (prefers-color-scheme: dark) {
     .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
     [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
     .darkmode-noBorder {border: 1px solid transparent !important;}
     [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
     }
  </style>
  <!--[if gte mso 9]>
  <style type="text/css">
     table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
  </style>
  <![endif]-->
</head>
<body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
  <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
  <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
  <tr>
     <td align="center" style="border-collapse: collapse;">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
  <tr>
     <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
        <br style="visibility: hidden;">
     </td>
  </tr>
  <tr>
     <td style="border-collapse: collapse;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
           <tr>
              <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                 <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                    <tr>
                       <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                             <tr>
                                <td align="left" style="border-collapse: collapse;">
                                   <a href="""+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                </td>
                             </tr>
                          </table>
                       </td>
                    </tr>
                 </table>
              </td>
           </tr>
        </table>
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
  <tr>
     <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
        <br style="visibility: hidden;">
     </td>
  </tr>
  <tr>
     <td>
        <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
  <tr>
     <td>
        <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
           <tr>
              <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
              <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                 <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                    <tr>
                       <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                       <td align="center" valign="top" style="border-collapse: collapse;">
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                             <tr>
                                <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                             <tr>
                                <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                               
                                </td>
                             </tr>
                             <tr>
                                <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                             <tr>
                                <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                   Sorry! Your project failed
                                </td>
                             </tr>
                             <tr>
                                <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                          </table>
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                             <tr>
                                <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 25px; padding-left: 0px; padding-right: 0px; padding-top: 25px;">
                                   <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/feeling_sorry_trans.png?raw=true" width="260" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                </td>
                             </tr>
                             <tr>
                                <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                             <tr>
                                <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                   We apologize that we were unable to complete your project due to a technical issue. Could you please try again?
                                </td>
                             </tr>
                             <tr>
                                <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                          </table>
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                             <tr>
                                <td align="center" style="border-collapse: collapse;" >
                                   <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                      <tr>
                                         <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                            <a href="""+str(os.environ["APP_URL"])+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                               style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">CREATE NEW PROJECT</span></a>
                                         </td>
                                      </tr>
                                   </table>
                                </td>
                             </tr>
                          </table>
                       </td>
                       <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                    <tr>
                       <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                          <br style="visibility: hidden;">
                       </td>
                    </tr>
                 </table>
              </td>
              <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
           </tr>
        </table>
  </tr>
  <tr>
     <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
        <br style="visibility: hidden;">
     </td>
  </tr>
  <tr>
     <td>
        <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
  <tr>
     <td>
        <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
           <tr>
              <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
              <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                 <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                    <tr>
                       <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                       <td align="center" valign="top" style="border-collapse: collapse;">
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                             <tr>
                                <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                             <tr>
                                <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
Scoretize, your fastest solution to measure your digital efficiency score across various digital channels against category and industry competitors.                                 </td>
                             </tr>
                          </table>
                       </td>
                       <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                    <tr>
                       <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                          <br style="visibility: hidden;">
                       </td>
                    </tr>
                 </table>
              </td>
              <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
           </tr>
        </table>
  </tr>
  <tr>
     <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
        <br style="visibility: hidden;">
     </td>
  </tr>
  <tr>
     <td>
        <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
           <tr>
              <td>
                 <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                    <tr>
                       <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                       <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                          <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                             <tr>
                                <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                <td align="center" valign="top" style="border-collapse: collapse;">
                                   <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                      <tr>
                                         <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                            <br style="visibility: hidden;">
                                         </td>
                                      </tr>
                                      <tr>
                                         <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                            Please do not hesitate to contact us
                                         </td>
                                      </tr>
                                      <tr>
                                         <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                            <br style="visibility: hidden;">
                                         </td>
                                      </tr>
                                      <tr>
                                         <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                            Do you require assistance? Please contact us via our website's live chat or via email at  <a style="color: inherit !important;" href="mailto: support@scoretize.com"> support@scoretize.com</a>
                                         </td>
                                      </tr>
                                   </table>
                                </td>
                                <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                             <tr>
                                <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                   <br style="visibility: hidden;">
                                </td>
                             </tr>
                          </table>
                       </td>
                       <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                    </tr>
                 </table>
           </tr>
        </table>
     </td>
  </tr>
  <tr>
     <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
        <br style="visibility: hidden;">
     </td>
  </tr>
  <tr>
     <td>
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
           <tr>
              <td>
                 <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                    <tr>
                       <td>
                          <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                             <tr>
                                <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                   <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                      <tr>
                                         <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                         <td align="center" valign="top" style="border-collapse: collapse;">
                                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                               <tr>
                                                  <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                     Follow us to stay updated
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                     <br style="visibility: hidden;">
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                     Help us improve by sharing your feedback in this short
                                                     <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                        style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                     <br style="visibility: hidden;">
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                     <br style="visibility: hidden;">
                                                  </td>
                                               </tr>
                                            </table>
                                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                               <tr>
                                                  <td class="footer-sm">
                                                     <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                        <tr>
                                                           <td align="center" valign="top" width="80px">
                                                              <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                           </td>
                                                           <td align="center" valign="top" width="80">
                                                              <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                           </td>
                                                           <td align="center" valign="top" width="80px">
                                                              <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                           </td>
                                                        </tr>
                                                     </table>
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                     <br style="visibility: hidden;">
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                     Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                     <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                     <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                  </td>
                                               </tr>
                                               <tr>
                                                  <td height="30" class="page-break" bgcolor="#f4f4f" 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
  <!--Help character display properly.-->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <!--Set the initial scale of the email.-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <!--Force Outlook clients to render with a better MS engine.-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge">
  <!--Help prevent blue links and autolinking-->
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
  <!--prevent Apple from reformatting and zooming messages.-->
  <meta name="x-apple-disable-message-reformatting">
  <!--target dark mode-->
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark only">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
  <title>Scoretize</title>
  <style type="text/css">
     body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
     #outlook a {
     padding: 0;
     }
     body {
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     background: white;
     width: 100% !important;
     -webkit-text-size-adjust: 100%;
     -ms-text-size-adjust: 100%;
     margin-top: 0px;
     margin-right: 0px;
     margin-bottom: 0px;
     margin-left: 0px;
     padding-top: 0px;
     padding-right: 0px;
     padding-bottom: 0px;
     padding-left: 0px;
     }
     .ExternalClass {
     width: 100%;
     }
     .ExternalClass * {
     line-height: 100%;
     }
     .ExternalClass,
     .ExternalClass p,
     .ExternalClass span,
     .ExternalClass font,
     .ExternalClass td,
     .ExternalClass div {
     line-height: 100%;
     }
     img {
     outline: none;
     text-decoration: none;
     -ms-interpolation-mode: bicubic;
     }
     a img {
     border: none;
     }
     .image-fix {
     display: block;
     }
     /*TYPOGRAPHY */
     .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
     .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
     .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
     .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
     .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
     .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
     .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
     .unsub-text {
     mso-line-height-rule: exactly;
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     font-size: 15px;
     line-height: 15px;
     font-weight: normal;
     text-decoration: none;
     color: #cbd0d6;
     }
     .unsub-text a {
     text-decoration: none;
     color: #cbd0d6;
     }
     .address-text {
     mso-line-height-rule: exactly;
     font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
     font-size: 15px;
     line-height: 15px;
     font-weight: normal;
     text-decoration: none;
     color: #cbd0d6;
     }
     .address-text a {
     text-decoration: none;
     color: #cbd0d6;
     }
     .emailButton{
     box-sizing: border-box;
     max-width:600px !important;
     width:100% !important;
     }
     .footer-sm {                  box-sizing: border-box;
     max-width:600px !important;
     width:100% !important;}
  </style>
  <!--mobile styles-->
  <style>
     @media screen and (max-width:600px) {
     .wFull { width: 100% !important; }
     .imgFull { width: 70% !important; height: auto !important; }
     .h1 {font-size: 26px !important; line-height: 36px !important;}
     .h2 {font-size: 24px !important; line-height: 32px !important;}
     .text-base {font-size: 20px !important; line-height: 28px !important;}
     .text-sm {font-size: 14px !important; line-height: 20px !important;}
     .text-xs {font-size: 12px !important; line-height: 16px !important;}
     .text-xxs {font-size: 11px !important; line-height: 16px !important;}
     .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
     .emailButton{
     max-width:100% !important;
     width:100% !important;
     }
     .emailButtonContent {
     padding-right: 10px !important;
     padding-left: 10px !important;
     }
     .emailButton a{
     display:block !important;
     font-size:17px !important;
     }
     }
     /*DARK MODE*/
     @media (prefers-color-scheme: dark) {
     .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
     [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
     .darkmode-noBorder {border: 1px solid transparent !important;}
     [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
     }
  </style>
  <!--[if gte mso 9]>
  <style type="text/css">
     table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
  </style>
  <![endif]-->
</head>
<body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
  <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
  <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
  <tr>
     <td align="center" style="border-collapse: collapse;">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
  <tr>

  </tr>
  <tr>
     <td style="border-collapse: collapse;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
           <tr>
              <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                 <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                    <tr>

                    </tr>
                 </table>
              </td>
           </tr>
        </table>
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
  <tr>

  </tr>
  <tr>
     <td>
        <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
  <tr>
     <td>
        <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
           <tr>



           </tr>
        </table>
  </tr>
  <tr>

  </tr>
  <tr>

           </tr>
        </table>
     </td>
  </tr>
</body>
</html>
    """
        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY,EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)
        
def send_mail_for_project_update(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['shrikrithika.srinivasan@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize', project='Project'):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE STYLES*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Check out your new project in Scoretize here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Hi """ +str(name[0].capitalize())+ """!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       New data available
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 25px; padding-left: 0px; padding-right: 0px; padding-top: 25px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/project_update_graphs.png?raw=true" width="260" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       We have updated your """+str(project)+""" project's score and KPIs.
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(os.environ["APP_URL"])+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">CHECK MY PROJECT</span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Your fastest solution to measure your digital efficiency score across various digital channels against category and industry competitors.
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Don’t hesitate to contact us
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Need any help? Please, send us a message in our live chat on the website, or email us at <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                             </td>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>"""

        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY,EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)


def send_mail_for_pitch_success(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['alejandra.elsin@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize', project='Project', project_id=""):
    try:
        base_url = os.environ["FRONTEND_BASE_URL"]
        pitch_deck_url = base_url + "pitch-deck/"
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE STYLES*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Check out your new project in Scoretize here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                      Exciting news!
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       Your pitch deck 
is completed successfully
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 0x; padding-left: 0px; padding-right: 0px; padding-top: 0px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/39178315b607066982928119fce8670854e18aae/email_resources/images/pitch_success.png?raw=true" width="360" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; background-color: transparent;">
                                    </td>
                                 </tr>
                                 <tr>
                                    
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Download your PowerPoint now
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(pitch_deck_url)+str(project)+"?id="+str(project_id)+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">VIEW RESULTS</span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                       <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Thank you for choosing Scoretize Pitch Deck service
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                We’re excited to embark on this journey with you and help showcase your company’s potential
                                             </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Don’t hesitate to contact us
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Need any help? Please, send us a message in our live chat on the website, or email us at <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                             </td>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>"""

        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY,EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)

def send_mail_for_pitch_failure(reset_token=None, text='Email_body', subject='Scoretize Support', from_email=EMAIL_NOTREPLY, to_emails=['alejandra.elsin@thekeenfolks.com'], message='Contact us at Scoretize support', name='Scoretize', project='Project', project_id=""):
    try:
        base_url = os.environ["FRONTEND_BASE_URL"]
        pitch_deck_url = base_url + "pitch-deck/"
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
   <head>
      <!--Help character display properly.-->
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <!--Set the initial scale of the email.-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <!--Force Outlook clients to render with a better MS engine.-->
      <meta http-equiv="X-UA-Compatible" content="IE=Edge">
      <!--Help prevent blue links and autolinking-->
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <!--prevent Apple from reformatting and zooming messages.-->
      <meta name="x-apple-disable-message-reformatting">
      <!--target dark mode-->
      <meta name="color-scheme" content="light dark">
      <meta name="supported-color-schemes" content="light dark only">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@100;400;500;600;700&family=Source+Sans+Pro:wght@200;300;400;600;700&display=swap" rel="stylesheet">
      <title>Scoretize</title>
      <style type="text/css">
         body,table,td,p,a { -ms-text-size-adjust: 100% !important; -webkit-text-size-adjust: 100% !important; }
         #outlook a {
         padding: 0;
         }
         body {
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         background: white;
         width: 100% !important;
         -webkit-text-size-adjust: 100%;
         -ms-text-size-adjust: 100%;
         margin-top: 0px;
         margin-right: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         padding-top: 0px;
         padding-right: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         }
         .ExternalClass {
         width: 100%;
         }
         .ExternalClass * {
         line-height: 100%;
         }
         .ExternalClass,
         .ExternalClass p,
         .ExternalClass span,
         .ExternalClass font,
         .ExternalClass td,
         .ExternalClass div {
         line-height: 100%;
         }
         img {
         outline: none;
         text-decoration: none;
         -ms-interpolation-mode: bicubic;
         }
         a img {
         border: none;
         }
         .image-fix {
         display: block;
         }
         /*TYPOGRAPHY */
         .h1 {font-size: 36px !important; line-height: 40px !important; mso-line-height-rule: exactly;}
         .h2 {font-size: 30px !important; line-height: 36px !important; mso-line-height-rule: exactly;}
         .text-base {font-size: 24px !important; line-height: 32px !important; mso-line-height-rule: exactly;}
         .text-sm {font-size: 28px !important; line-height: 28px !important; mso-line-height-rule: exactly;}
         .text-xs {font-size: 18px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .text-xxs {font-size: 14px !important; line-height: 20px !important; mso-line-height-rule: exactly;}
         .btn, .btn-inner {font-size: 22px !important; line-height: 50px !important; mso-line-height-rule: exactly;}
         .unsub-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .unsub-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text {
         mso-line-height-rule: exactly;
         font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;
         font-size: 15px;
         line-height: 15px;
         font-weight: normal;
         text-decoration: none;
         color: #cbd0d6;
         }
         .address-text a {
         text-decoration: none;
         color: #cbd0d6;
         }
         .emailButton{
         box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;
         }
         .footer-sm {                  box-sizing: border-box;
         max-width:600px !important;
         width:100% !important;}
      </style>
      <!--mobile styles-->
      <style>
         @media screen and (max-width:600px) {
         .wFull { width: 100% !important; }
         .imgFull { width: 70% !important; height: auto !important; }
         .h1 {font-size: 26px !important; line-height: 36px !important;}
         .h2 {font-size: 24px !important; line-height: 32px !important;}
         .text-base {font-size: 20px !important; line-height: 28px !important;}
         .text-sm {font-size: 14px !important; line-height: 20px !important;}
         .text-xs {font-size: 12px !important; line-height: 16px !important;}
         .text-xxs {font-size: 11px !important; line-height: 16px !important;}
         .btn, .btn-inner {font-size: 20px !important; line-height: 25px !important;}
         .emailButton{
         max-width:100% !important;
         width:100% !important;
         }
         .emailButtonContent {
         padding-right: 10px !important;
         padding-left: 10px !important;
         }
         .emailButton a{
         display:block !important;
         font-size:17px !important;
         }
         }
         /*DARK MODE STYLES*/
         @media (prefers-color-scheme: dark) {
         .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         [data-ogsc] .darkmode-border {border: 1px solid transparent !important; background-color: transparent !important;}
         .darkmode-noBorder {border: 1px solid transparent !important;}
         [data-ogsc] .darkmode-noBorder {border: 1px solid transparent !important;}
         }
      </style>
      <!--[if gte mso 9]>
      <style type="text/css">
         table, tr, td { border-spacing: 0 !important; mso-table-lspace: 0px !important; mso-table-rspace: 0pt !important; border-collapse: collapse !important; mso-line-height-rule:exactly !important;}
      </style>
      <![endif]-->
   </head>
   <body class="colored" style="-ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; background: white; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px; width: 100%;">
      <div class="litmus-builder-preview-text" style="display:none;font-size:1px;color:#333333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">Check out your new project in Scoretize here&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
      <table role="presentation" bgcolor="#eeeeee" width="100%" cellspacing="0" cellpadding="0" border="0" class="table-body" style="line-height: 100%; margin: 0; padding: 0; width: 100%;">
      <tr>
         <td align="center" style="border-collapse: collapse;">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" align="center" class="content-table wFull">
      <tr>
         <td height="10" class="page-break" bgcolor="#eeeeee" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td style="border-collapse: collapse;">
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff" align="left">
               <tr>
                  <td align="left" style="border-collapse: collapse;" style="background-color: #fff">
                     <table role="presentation" width="580" border="0" cellspacing="0" cellpadding="0" class="content-table" align="left">
                        <tr>
                           <td width="150" valign="top" align="right" class="header-block-l" style="border-collapse: collapse; padding-bottom: 10px; padding-left: 15px; padding-right: 0px; padding-top: 10px;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                                 <tr>
                                    <td align="left" style="border-collapse: collapse;">
                                       <a href="""+str(os.environ["APP_URL"])+""" style="color: black; text-decoration: underline;"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/logo.png?raw=true" width="165" height="60" alt="Scoretize Logo" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none; max-width: 165px;"></a>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
      <tr>
         <td height="10" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                      Failure has been encountered
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="h1" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 34px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                       Unsuccessful pitch deck 
generation
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" valign="top" class="top-video-image" style="border-collapse: collapse; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 0px;">
                                       <img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/39178315b607066982928119fce8670854e18aae/email_resources/images/pitch_failed.png?raw=true" width="360" alt="" class="image-fix" style="-ms-interpolation-mode: bicubic; display: block; outline: none; text-decoration: none;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Click the button below to restart the generation of the Pitch Deck
                                    </td>
                                 </tr>
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td align="center" style="border-collapse: collapse;" >
                                       <table border="0" cellpadding="0" cellspacing="0" class="emailButton"  bgcolor="#5858D6" style="-moz-border-radius: 7px; -webkit-border-radius: 7px; border-collapse: collapse; border-radius: 7px; background-color:#5858D6;">
                                          <tr>
                                             <td align="center" valign="middle" class="emailButtonContent" style="padding-top:20px; padding-right:30px; padding-bottom:20px; padding-left:30px; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;">
                                                <a href="""+str(pitch_deck_url)+str(project)+"?id="+str(project_id)+""" style="color: white; display: inline-block; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 22px; font-weight: 600 ;text-decoration: none; width: 100%;"><span
                                                   style="color: white; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial;"> PITCH DECK GENERATION </span></a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
               <tr>
                  <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                  <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#f4f4f4" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #f4f4f4">
                     <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                        <tr>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                           <td align="center" valign="top" style="border-collapse: collapse;">
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                 <tr>
                                    <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                                 <tr>
                                    <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                       Your fastest solution to measure your digital efficiency score across various digital channels against category and industry competitors.
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td align="center" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                        <tr>
                           <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color:#f4f4f4;">
                              <br style="visibility: hidden;">
                           </td>
                        </tr>
                     </table>
                  </td>
                  <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
               </tr>
            </table>
      </tr>
      <tr>
         <td height="40" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table cellpadding="0" cellspacing="0" border="0" width="600" align="center" class="fluid-table">
               <tr>
                  <td>
                     <table width="600" align="left" border="0" cellpadding="0" cellspacing="0" class="fluid-table">
                        <tr>
                           <td width="30" bgcolor="#fff" style="background-color: #fff"></td>
                           <td width="400" align="center"  class="darkmode-noBorder" bgcolor="#fff" style="color:#000000; text-decoration:none; -moz-border-radius: 15px; -webkit-border-radius: 15px; background-clip: padding-box; border-radius: 15px; border: 4px solid #f4f4f4; background-color: #fff">
                              <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                 <tr>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;"> </td>
                                    <td align="center" valign="top" style="border-collapse: collapse;">
                                       <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                          <tr>
                                             <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 36px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                Don’t hesitate to contact us
                                             </td>
                                          </tr>
                                          <tr>
                                             <td height="20" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                                <br style="visibility: hidden;">
                                             </td>
                                          </tr>
                                          <tr>
                                             <td align="center" valign="top" class="text-base" style="border-collapse: collapse; color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 24px; letter-spacing: 1px; font-weight: 300; line-height: 32px; mso-line-height-rule: exactly; text-decoration: none;">
                                                Need any help? Please, send us a message in our live chat on the website, or email us at <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a>
                                             </td>
                                          </tr>
                                       </table>
                                    </td>
                                    <td align="center" valign="top" style="border-collapse: collapse; width:15px;" > </td>
                                 <tr>
                                    <td height="30" class="page-break" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly;">
                                       <br style="visibility: hidden;">
                                    </td>
                                 </tr>
                              </table>
                           </td>
                           <td width="30"  bgcolor="#fff" style="background-color: #fff"></td>
                        </tr>
                     </table>
               </tr>
            </table>
         </td>
      </tr>
      <tr>
         <td height="60" class="page-break" bgcolor="#fff" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #fff">
            <br style="visibility: hidden;">
         </td>
      </tr>
      <tr>
         <td>
            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
               <tr>
                  <td>
                     <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#fff">
                        <tr>
                           <td>
                              <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f4f4f4" style="background-color: #f4f4f4;">
                                 <tr>
                                    <td class="top-video-padding" align="center" valign="top" style="border-collapse: collapse; padding-bottom: 40px; padding-left: 0px; padding-right: 0px; padding-top: 40px;">
                                       <table role="presentation" width="460" border="0" cellspacing="0" cellpadding="0" class="video-table">
                                          <tr>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                             <td align="center" valign="top" style="border-collapse: collapse;">
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td align="center" valign="top" class="h2" style="border-collapse: collapse; color: #20234E; font-family: 'Archivo', 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 30px; font-weight: 600; line-height: 30px; mso-line-height-rule: exactly; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; padding-top: 10px; text-decoration: none;">
                                                         Follow us to stay updated
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="20" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 18px; letter-spacing: 1px; font-weight: 400; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Help us improve by sharing your feedback in this short
                                                         <span class="text-xs" style="color: #20234E; font-family: 'Source Sans Pro', sans-serif, 'Trebuchet MS', Arial; font-size: 18px; font-weight: 500; line-height: 28px; mso-line-height-rule: exactly; text-decoration: none;"><a  class="text-xs" href="https://thekeenfolks.typeform.com/scoretize"
                                                            style="color: #20234E; text-decoration: underline; font-size: 18px; font-weight: 400; line-height: 15px; mso-line-height-rule: exactly;">survey.</a></span>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="10" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4;">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                   <tr>
                                                      <td class="footer-sm">
                                                         <table border="0" cellpadding="0" cellspacing="0" role="presentation" align="center" width="250">
                                                            <tr>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.instagram.com/scoretize_/" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/instagram-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Instagram" width="38" height="38" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80">
                                                                  <a href="https://www.facebook.com" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/linkedin-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize LinkedIn" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                               <td align="center" valign="top" width="80px">
                                                                  <a href="https://www.facebook.com/scoretize" target="_blank"><img src="https://github.com/TheKeenfolksDigital/Scoretize_resources/blob/dev/email_resources/images/facebook-free-icon-font.png?raw=true" class="fadeimg" alt="Scoretize Facebook" width="40" height="40" style="font-size: 12px; line-height: 14px; font-family: 'Source Sans Pro', 'Trebuchet MS' Arial, sans-serif; color: #028383;" /></a>
                                                               </td>
                                                            </tr>
                                                         </table>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="40" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4; ">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top"  class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         Copyright © 2022 <b>Scoretize</b>. All Rights Reserved.
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> support@scoretize.com</a> | <a style="color: inherit; text-decoration: none" href="tel:+34605351325">+34 605 351 325</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td align="center" valign="top" class="text-xxs" style="border-collapse: collapse; color: #20234E; font-family: Arial, 'Trebuchet MS' Arial, sans-serif; font-size: 14px; letter-spacing: 1px; font-weight: 300; line-height: 20px; mso-line-height-rule: exactly; text-decoration: none;">
                                                         <a style="color: inherit" href="mailto:support@scoretize.com"> Unsubscribe</a>
                                                      </td>
                                                   </tr>
                                                   <tr>
                                                      <td height="30" class="page-break" bgcolor="#f4f4f4" style="border-collapse: collapse; line-height: 10px; mso-line-height-rule: exactly; background-color: #f4f4f4">
                                                         <br style="visibility: hidden;">
                                                      </td>
                                                   </tr>
                                                </table>
                                             </td>
                                             <td align="center" bgcolor="#f4f4f4" valign="top" style="border-collapse: collapse; width:15px; background: #f4f4f4" > </td>
                                          </tr>
                                       </table>
                                    </td>
                                 </tr>
                              </table>
                        </tr>
                     </table>
                  </td>
               </tr>
            </table>
         </td>
      </tr>
   </body>
</html>"""

        part1 = MIMEText(html, 'html')
        msg.attach(part1)
        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.office365.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_NOTREPLY,EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
    except IntegrityError as e:
        bad_request('Email sending failed', 'Email sending failed', e)
        print("email sending failed")

