<script>
	import { page } from '$app/state';

	import Nav from './footer.nav.svelte';
	import Contact from './footer.contact.svelte';
	import Socials from './footer.socials.svelte';
	import Form from './footer.form.svelte';

	import { Content } from '$lib/layout';
</script>

{#if page.url.pathname != '/post'}
	<hr />
{/if}

<Content --content-height="100%" --content-padding-top="56px" --content-padding-bottom="56px">
	<footer id="footer">
		<div class="page_title">Get In Touch</div>

		<section>
			<div class="form">
				Got a question or proposal, or just want to say hello? Please go ahead.
				<br />
				<br />

				<Form />
			</div>
			<div class="contact">
				<Contact />
				<br /><br />
				<Socials />
				<br /><br />
				<hr />
				<br /><br />
				<Nav />
			</div>
		</section>
		<div class="copyright">&copy 2025 | Designed & Built by Theophilus Ogbolu.</div>
	</footer>
</Content>

<style>
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

	.form,
	.contact {
		width: 100%;
	}
	.copyright {
		text-align: center;
	}
</style>
