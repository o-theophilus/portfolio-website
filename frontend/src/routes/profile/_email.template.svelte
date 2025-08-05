<script>
	import { EmailTemplate } from '$lib/layout';
</script>

<EmailTemplate>
	<b> Dear {'{'}name{'}'}, </b>
	<br />
	<br />
	To change your email, please use the following Code:
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
	<br />
	Please enter this Code on the email change form to validate your request. Please note that the Code
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
	<b> Theophilus Ogbolu</b>
</EmailTemplate>
