<script>
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Dear {'{'}name{'}'}, </b>
	<br />
	<br />
	To change your password, please use the following One-Time Password (OTP):
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
	Please enter this OTP on the password change form to validate your request. Please note that the OTP
	is only valid for a limited time.
	<br />
	<br />
	If you did not request this change, please disregard this message.
	<br />
	<br />
	If you have any questions or need further assistance, please don't hesitate to reach out to me.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Theophilus </b>
</Template>
