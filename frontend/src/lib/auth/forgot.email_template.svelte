<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
</script>

<EmailTemplate>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	To reset your password, please use the following Code:
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
		<b> {'{'}code{'}'} </b>
	</div>
	<br />
	Please enter this Code on the password reset form to validate your request. Please note that the Code
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
	<b> Theophilus Ogbolu </b>
</EmailTemplate>
