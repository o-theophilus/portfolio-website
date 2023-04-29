<script>
	import { _user, api_url } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

	import Template from '$lib/email_template.forgot.svelte';

	// export let data;
	let user = {};
</script>

<Meta title={user.name} description="This page displays the user profile" />

<Content>
	<!-- <Button class="secondary" on:click={async () => {}}>Logout</Button> -->
	<Template />
</Content>

<style>
</style>
