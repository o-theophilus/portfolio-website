<script>
	import { page } from '$app/stores';

	import Nav from './footer.nav.svelte';
	import Contact from './footer.contact.svelte';
	import Socials from './footer.socials.svelte';
	import Form from './footer.form.svelte';

	import Content from '$lib/content.svelte';
</script>

<Content fit>
	{#if $page.url.pathname != '/post'}
		<hr />
	{/if}
	<footer id="footer">
		<div class="ititle"><strong> Get in touch! </strong></div>

		Whether you have an idea for a project or just want to chat, feel free to shoot me an email!

		<br />
		Got a question or proposal, or just want to say hello? Go ahead.

		<section>
			<div class="form">
				<Form />
			</div>
			<div>
				<Contact />
				<br /><br />
				<Socials />
				<br /><br />
				<hr />
				<br /><br />
				<Nav />
			</div>
		</section>
		<div class="copyright">&copy 2024 | Designed & Built by Theophilus Ogbolu.</div>
		<br /><br /><br />
	</footer>
</Content>

<style>
	.ititle {
		margin: var(--sp3) 0;
	}

	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp4);
		margin: var(--sp3) 0;
	}
	.copyright {
		margin-top: var(--sp4);
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
</style>
