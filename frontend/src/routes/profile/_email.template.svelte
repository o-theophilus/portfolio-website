<script>
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Dear {'{'}name{'}'}, </b>
	<br />
	<br />
	Thank you for initiating the process to change your email address on Meji. To proceed with the email
	change, please use the following One-Time Password (OTP):
	<br />
	<br />
	<div
		style="
		text-align: center;
		font-size: x-large;
		padding: 16px;
		border: 2px solid #efefef;
		border-radius: 4px;
	"
	>
		<b> {'{'}otp{'}'} </b>
	</div>
	<br />
	<br />
	Please enter this OTP on the email change form to validate your request. Please note that the OTP is
	only valid for a limited time.
	<br />
	<br />
	If you did not request this change, please disregard this message. The security of your account is
	important to us, and we advise you to contact our customer support immediately if you suspect any unauthorized
	activity.
	<br />
	<br />
	Thank you for being a valued customer. If you have any questions or need further assistance, please
	don't hesitate to reach out to our customer support team.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
