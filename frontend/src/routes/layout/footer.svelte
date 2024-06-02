<script>
	import { page } from '$app/stores';

	import Nav from './footer.nav.svelte';
	import Contact from './footer.contact.svelte';
	import Socials from './footer.socials.svelte';
	import Form from './footer.form.svelte';

	import Content from '$lib/content.svelte';
</script>

<Content>
	{#if $page.url.pathname != '/post'}
		<hr />
	{/if}
	<footer id="footer">
		<div class="title">Get in touch!</div>
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
		<div class="copyright">&copy Loup 2023. All rights reserved.</div>
		<br /><br />
	</footer>
</Content>

<style>
	.title {
		margin: var(--sp4) 0;

		font-size: x-large;
		font-weight: 800;
	}

	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp5);
		margin: var(--sp4) 0;
	}
	.copyright {
		margin: var(--sp5) 0;
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
