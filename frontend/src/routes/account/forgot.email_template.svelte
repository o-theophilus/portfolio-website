<script>
	import { page } from '$app/stores';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	To reset your password, please use the following One-Time Password (OTP):
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
	Please enter this OTP on the password change form to validate your request.
	<br />
	<br />

	Note:
	<ul>
		<li>
			This OTP will be valid for 15 minutes.
		</li>

		<li>If you did not request this change, please disregard this message.</li>
	</ul>
	<br />
	If you have any questions or concerns, please feel free to contact me.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Theophilus. </b>
</Template>
