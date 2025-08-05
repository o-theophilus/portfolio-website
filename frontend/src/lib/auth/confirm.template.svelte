<script>
	import { EmailTemplate } from '$lib/layout';
</script>

<EmailTemplate>
	<b>Hello {'{'}name{'}'},</b>
	<br /><br />
	Welcome to my portfolio website! Thank you for signing up. I'm excited to have you as part of my community.
	You'll find my latest works and blog posts on design, development, and industry trends. I hope you
	find it inspiring and informative.
	<br /><br />
	To complete you signup, please confirm your email address using the Code below:
	<br /><br />
	<div
		style="
		text-align: center;
		font-size: x-large;
		padding: 16px;
		border: 2px solid #efefef;
		border-radius: 4px;
	"
	>
		<b>{'{'}code{'}'}</b>
	</div>
	<br /><br />
	Enter this Code on the confirmation form. Note that it is valid for a limited time. If you didn't request
	this, please disregard this message.
	<br /><br />
	If you have any questions or comments, feel free to reach out. I'd love to hear from you. Thank you
	again for joining. I look forward to connecting with you!
	<br /><br />
	Best regards,
	<br /><br />
	<b>Theophilus Ogbolu</b>
</EmailTemplate>
