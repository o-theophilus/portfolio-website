<script>
	import { page } from '$app/stores';

	import Nav from './footer.nav.svelte';
	import Contact from './footer.contact.svelte';
	import Socials from './footer.socials.svelte';
	import Form from './footer.form.svelte';

	import Content from '$lib/content.svelte';
</script>

{#if $page.url.pathname != '/post'}
	<hr />
{/if}

<Content fit>
	<footer id="footer">
		<div class="ititle"><strong> Get In Touch </strong></div>

		<section>
			<div class="form">
				Got a question or proposal, or just want to say hello? Please go ahead.
				<br />
				<br />

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
		margin-top: var(--sp5);
		margin-bottom: var(--sp3);
	}

	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp4);
		margin: var(--sp3) 0;
	}
	.copyright {
		margin-top: var(--sp5);
		font-size: 0.8rem;
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
