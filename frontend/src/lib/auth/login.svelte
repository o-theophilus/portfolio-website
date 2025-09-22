<script>
	import { page } from '$app/state';

	import { module, loading, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button, Link } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Icon } from '$lib/macro';
	import Signup from './signup.svelte';
	import Forgot from './forgot_1.email.svelte';
	import EmailTemplate from './confirm.template.svelte';
	import Confirm from './confirm.svelte';

	let email_template;

	let form = $state({
		email: module.value.email,
		remember: false
	});
	let error = $state({});

	let return_url = page.url.pathname;
	if (module.value.return_url) {
		return_url = module.value.return_url;
	}

	const validate = () => {
		error = {};

		if (!form.email) {
			error.email = 'This field is required';
		}
		if (!form.password) {
			error.password = 'This field is required';
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		form.email_template = email_template.innerHTML.replace(/&amp;/g, '&');

		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});

		resp = await resp.json();
		if (resp.status != 200) {
			loading.close();
		}

		if (resp.status == 200) {
			app.token = resp.token;
			app.login = true;
			app.user = {};
			document.location = return_url;
		} else if (resp.error == 'not confirmed') {
			module.open(Confirm, { email: form.email });
		} else {
			error = resp;
		}
	};
</script>

<Form title="Login" error={error.error}>
	<IG
		name="Email or Username"
		icon="mail"
		error={error.email}
		type="email"
		bind:value={form.email}
		placeholder="Email or Username here"
	/>

	<IG
		name="Password"
		icon="key-round"
		error={error.password}
		placeholder="Password here"
		type="password+"
		bind:value={form.password}
	></IG>

	<IG>
		{#snippet input()}
			<div
				class="custom-checkbox"
				onclick={() => (form.remember = !form.remember)}
				role="presentation"

			>
				<div class="checkbox" class:active={form.remember}>
					<div class="icon">
						<Icon icon="check"></Icon>
					</div>
				</div>
				Remember me
			</div>
		{/snippet}
	</IG>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>

	<br />
	<br />

	<div class="line">
		<Link onclick={() => module.open(Signup, { email: form.email })} --link-font-size="0.8rem">
			Signup
		</Link>
		<span class="divider"> | </span>
		<Link onclick={() => module.open(Forgot, { email: form.email })} --link-font-size="0.8rem">
			Forgot Password
		</Link>
	</div>
</Form>

<div bind:this={email_template} style="display: none;">
	<EmailTemplate />
</div>

<style>
	.line {
		gap: 16px;
	}

	.custom-checkbox {
		display: flex;
		align-items: center;
		gap: 16px;
		font-size: 0.8rem;
		width: max-content;
	}

	.checkbox {
		--size: 20px;
		position: relative;

		width: var(--size);
		height: var(--size);
		border-radius: 4px;
		outline: 2px solid var(--input);
		outline-offset: -2px;

		background-color: var(--input);
		cursor: pointer;

		transition: background-color var(--trans);
	}

	.checkbox:hover{
		outline-color: var(--ft1);
	}
	.active {
		background-color: var(--cl1);
	}

	.icon {
		position: absolute;
		inset: 0;

		display: flex;
		align-items: center;
		justify-content: center;
		color: transparent;

		transition: color var(--trans);
	}
	.active .icon {
		color: white;
	}
</style>
