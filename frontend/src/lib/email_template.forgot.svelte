<script>
	import { page } from '$app/stores';
	import Template from './email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	We have received a request to reset your password.

	<span
		style="
	color: red;"
	>
		If you did not initiate this action, please disregard this email.
	</span>
	<br />
	<br />

	To reset your password, please click on the link below:
	<br />
	<br />
	<a
		href="{$page.url.origin}/?module=password&token={'{'}token{'}'}"
		style="
	display: block;
	padding: 16px;
	text-decoration: none;
	text-align: center;
	border-radius: 4px;
	border: none;
	color: white;
	background: linear-gradient(0deg, rgb(0, 113, 0) 0%, rgb(0, 177, 0) 100%);"
	>
		<b> Reset your password </b>
	</a>
	<br />
	If you have any trouble clicking the button above, please copy and paste the URL below into your web
	browser.
	<br />
	<br />
	{$page.url.origin}/?module=password&token={'{'}token{'}'}
	<br />
	<br />

	If you have any questions or concerns, please feel free to contact us.
	<br />
	<br />

	Best regards,
	<br />
	<br />
	Theophilus.
	<br />
	<br />

	<span
		style="
	font-size: x-small;
	color: grey;"
	>
		Note: This link will expire in 1 hour for security reasons. If you do not reset your password
		within this time, you will need to submit another request.
	</span>
</Template>
