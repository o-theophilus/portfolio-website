<script>
	import Nav from './nav.svelte';

	import Contact from './contact.svelte';
	import Socials from './socials.svelte';
	import Form from './form/index.svelte';

	import Content from '$lib/comp/content.svelte';
</script>

<Content>
	<footer id="footer">
		<strong class="big">Get in touch!</strong>
		<br /><br /><br /><br />
		<section>
			<div class="form">
				<Form />
			</div>
			<div>
				<Contact />
				<br /><br /><br /><br />
				<Socials />
			</div>
		</section>
		<br /><br /><br /><br />
		<div class="copyright">&copy Incept 2021. All rights reserved.</div>
		<br /><br />
		<Nav />
	</footer>
</Content>

<style>
	footer {
		margin-top: var(--gap5);
		padding: var(--gap5) 0;
		border-top: 2px solid var(--mid_color);
	}

	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap5);
	}
	@media screen and (min-width: 900px) {
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
