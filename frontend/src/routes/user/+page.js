import { redirect } from '@sveltejs/kit';

export const load = async ({ parent }) => {
    const { data } = await parent()
    
    if(!data.locals.user.login){
        throw redirect(307, '/?module=login');
    }
}