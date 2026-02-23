<script>
	import Contact from './footer.contact.svelte';
	import Form from './footer.form.svelte';
	import Nav from './footer.nav.svelte';
	import Socials from './footer.socials.svelte';

	import { Content } from '$lib/layout';
</script>

<footer id="footer">
	<Content
		--content-height="auto"
		--content-padding-top="56px"
		--content-padding-bottom="56px"
		--content-background-color="var(--bg)"
	>
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
		<div class="copyright">&copy 2026 | Designed & Built by Theophilus Ogbolu.</div>
	</Content>
</footer>

<style>
footer{
	border-top: 1px solid var(--ol);
}
	section {
		display: flex;
		flex-direction: column;
		gap: 64px;
		margin: 24px 0;
	}
	.copyright {
		margin-top: 80px;
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
