<script>
	import Nav from './footer.nav.svelte';

	import Contact from './footer.contact.svelte';
	import Socials from './footer.socials.svelte';
	import Form from './footer.form.svelte';

	import Content from '$lib/content.svelte';
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
		<div class="copyright">&copy Loup 2023. All rights reserved.</div>
		<br /><br />
	</footer>
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp5);
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
		color: var(--ac1);
	}
</style>
