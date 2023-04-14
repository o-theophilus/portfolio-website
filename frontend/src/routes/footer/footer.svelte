<script>
	import Nav from './nav.svelte';

	import Contact from './contact.svelte';
	import Socials from './socials.svelte';
	import Form from './form.svelte';

	import Content from '$lib/comp/content.svelte';
</script>

<Content>
	<div class="hr v2" />
	<br /><br />
	<footer id="footer">
		<strong class="big">Get in touch!</strong>
		<br /><br />
		<section>
			<div class="form">
				<Form />
			</div>
			<div>
				<Contact />
				<br /><br />
				<Socials />
				<br /><br />
				<div class="hr" />
				<br /><br />
				<Nav />
			</div>
		</section>
		<br /><br />
		<div class="copyright">&copy Designdev 2021. All rights reserved.</div>
		<br /><br />
	</footer>
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap5);
	}
	@media screen and (min-width: 600px) {
		section {
			flex-direction: unset;
		}
	}

	.form {
		width: 100%;
	}
	.copyright {
		text-align: center;
	}
	.big {
		color: var(--accent1);
	}

</style>
