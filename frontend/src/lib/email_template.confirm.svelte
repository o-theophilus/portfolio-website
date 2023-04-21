<script>
	import { page } from '$app/stores';
	import Template from './email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	Thanks for signing up with Designdev! Before you get started shopping on Designdev, we need you to
	confirm your email address. Please click the button below to complete your signup.
	<br />
	<br />
	<a
		href="{$page.url.origin}/?module=confirm&token={'{'}token{'}'}"
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
		<b> Confirm Email Address </b>
	</a>
	<br />
	If you have any trouble clicking the button above, please copy and paste the URL below into your web
	browser.
	<br />
	<br />
	{$page.url.origin}/?module=confirm&token={'{'}token{'}'}
</Template>
