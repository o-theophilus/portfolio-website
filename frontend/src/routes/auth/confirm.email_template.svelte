<script>
	import { page } from '$app/stores';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	I wanted to personally welcome you to my portfolio website and thank you for signing up! I am thrilled
	to have you as a member of my community.
	<br />
	<br />
	To get started, we need you to confirm your email address. Please click the button below to complete
	your signup:
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
	<br />
	<br />
	On my portfolio website, you will find a collection of my latest works, as well as a blog where I share
	my thoughts on design, development, and industry trends. I hope you find it inspiring and informative!
	<br />
	<br />

	If you have any questions or comments, please don't hesitate to reach out to me. I would love to
	hear from you.
	<br />
	<br />

	Thank you again for joining my community. I look forward to connecting with you!
	<br />
	<br />

	Best regards,
	<br />
	<br />
	Theophilus.
</Template>
