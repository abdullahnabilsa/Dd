#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_2.py
================
Phase 2: Authentication & Roles
Creates auth hooks, login/register forms, route guard, and auth pages.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    """Create a file with the given path and content, creating directories as needed."""
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 2: Authentication & Roles")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # Common UI components needed by auth
    # ──────────────────────────────────────────────
    print("\n📁 Prerequisite: Common UI Components")
    print("-" * 40)

    # components/common/LoadingSpinner.tsx
    create_file("components/common/LoadingSpinner.tsx", """// مكون مؤشر التحميل: يعرض دائرة دوارة مع نص اختياري
'use client';

import { cn } from '@/utils/cn';

/**
 * خصائص مكون مؤشر التحميل
 */
interface LoadingSpinnerProps {
  /** الحجم */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** النص المرافق */
  text?: string;
  /** أسماء أصناف إضافية */
  className?: string;
  /** ملء الشاشة بالكامل */
  fullScreen?: boolean;
}

/**
 * أحجام المؤشر
 */
const sizeClasses = {
  sm: 'h-4 w-4 border-2',
  md: 'h-8 w-8 border-2',
  lg: 'h-12 w-12 border-3',
  xl: 'h-16 w-16 border-4',
} as const;

/**
 * مكون مؤشر التحميل
 */
export function LoadingSpinner({
  size = 'md',
  text,
  className,
  fullScreen = false,
}: LoadingSpinnerProps) {
  const spinner = (
    <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
      <div
        className={cn(
          'animate-spin rounded-full border-primary-500 border-t-transparent',
          sizeClasses[size]
        )}
        role="status"
        aria-label="Loading"
      />
      {text && (
        <p className="text-sm text-gray-500 dark:text-gray-400 animate-pulse">
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-modal flex items-center justify-center bg-white/80 dark:bg-dark-950/80 backdrop-blur-sm">
        {spinner}
      </div>
    );
  }

  return spinner;
}
""")

    # components/common/Logo.tsx
    create_file("components/common/Logo.tsx", """// مكون الشعار: يعرض شعار التطبيق مع الاسم
'use client';

import { cn } from '@/utils/cn';
import { Bot } from 'lucide-react';

/**
 * خصائص مكون الشعار
 */
interface LogoProps {
  /** الحجم */
  size?: 'sm' | 'md' | 'lg';
  /** إظهار النص */
  showText?: boolean;
  /** أسماء أصناف إضافية */
  className?: string;
}

/**
 * أحجام الشعار
 */
const iconSizes = {
  sm: 'h-6 w-6',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
} as const;

const textSizes = {
  sm: 'text-lg',
  md: 'text-xl',
  lg: 'text-3xl',
} as const;

/**
 * مكون الشعار
 */
export function Logo({ size = 'md', showText = true, className }: LogoProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="relative">
        <div className="absolute inset-0 bg-primary-500/20 rounded-xl blur-lg" />
        <div className="relative flex items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 p-2">
          <Bot className={cn('text-white', iconSizes[size])} />
        </div>
      </div>
      {showText && (
        <span
          className={cn(
            'font-bold bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent',
            textSizes[size]
          )}
        >
          {process.env.NEXT_PUBLIC_APP_NAME ?? 'AI Chat'}
        </span>
      )}
    </div>
  );
}
""")

    # components/common/ErrorMessage.tsx
    create_file("components/common/ErrorMessage.tsx", """// مكون رسالة الخطأ: يعرض رسالة خطأ مع أيقونة
'use client';

import { cn } from '@/utils/cn';
import { AlertCircle, X } from 'lucide-react';
import { useState } from 'react';

/**
 * خصائص مكون رسالة الخطأ
 */
interface ErrorMessageProps {
  /** رسالة الخطأ */
  message: string;
  /** قابل للإغلاق */
  dismissible?: boolean;
  /** أسماء أصناف إضافية */
  className?: string;
  /** عند الإغلاق */
  onDismiss?: () => void;
}

/**
 * مكون رسالة الخطأ
 */
export function ErrorMessage({
  message,
  dismissible = false,
  className,
  onDismiss,
}: ErrorMessageProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed || !message) return null;

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss?.();
  };

  return (
    <div
      className={cn(
        'flex items-start gap-3 rounded-lg border border-red-200 dark:border-red-800/50 bg-red-50 dark:bg-red-900/20 p-3 text-sm text-red-700 dark:text-red-300',
        className
      )}
      role="alert"
    >
      <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
      <p className="flex-1">{message}</p>
      {dismissible && (
        <button
          onClick={handleDismiss}
          className="shrink-0 rounded-md p-0.5 hover:bg-red-100 dark:hover:bg-red-800/30 transition-colors"
          aria-label="Dismiss error"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
""")

    # Shadcn UI base components needed
    create_file("components/ui/button.tsx", """// مكون الزر: زر قابل للتخصيص مع متغيرات وأحجام متعددة
'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils/cn';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-dark-950 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]',
  {
    variants: {
      variant: {
        default:
          'bg-primary-500 text-white shadow-md hover:bg-primary-600 hover:shadow-lg',
        destructive:
          'bg-red-500 text-white shadow-md hover:bg-red-600 hover:shadow-lg',
        outline:
          'border border-gray-200 dark:border-dark-600 bg-transparent hover:bg-gray-100 dark:hover:bg-dark-800 text-gray-700 dark:text-gray-300',
        secondary:
          'bg-gray-100 dark:bg-dark-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-dark-700',
        ghost:
          'hover:bg-gray-100 dark:hover:bg-dark-800 text-gray-700 dark:text-gray-300',
        link: 'text-primary-500 underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-8 px-3 text-xs',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
        'icon-sm': 'h-8 w-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** حالة التحميل */
  isLoading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, disabled, children, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        )}
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
""")

    create_file("components/ui/input.tsx", """// مكون حقل الإدخال: حقل نص قابل للتخصيص مع دعم RTL
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** رسالة الخطأ */
  error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          type={type}
          className={cn(
            'flex h-10 w-full rounded-lg border bg-white dark:bg-dark-900 px-3 py-2 text-sm',
            'border-gray-200 dark:border-dark-600',
            'text-gray-900 dark:text-gray-100',
            'placeholder:text-gray-400 dark:placeholder:text-gray-500',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'transition-colors duration-200',
            'file:border-0 file:bg-transparent file:text-sm file:font-medium',
            error && 'border-red-500 dark:border-red-500 focus:ring-red-500',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="mt-1 text-xs text-red-500 dark:text-red-400">{error}</p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };
""")

    create_file("components/ui/label.tsx", """// مكون التسمية: تسمية حقول النماذج
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  /** مطلوب */
  required?: boolean;
}

const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, children, required, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(
          'text-sm font-medium text-gray-700 dark:text-gray-300 leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
          className
        )}
        {...props}
      >
        {children}
        {required && <span className="text-red-500 ltr:ml-1 rtl:mr-1">*</span>}
      </label>
    );
  }
);
Label.displayName = 'Label';

export { Label };
""")

    create_file("components/ui/card.tsx", """// مكون البطاقة: حاوية بطاقة مع رأس ومحتوى وتذييل
'use client';

import * as React from 'react';
import { cn } from '@/utils/cn';

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'rounded-xl border border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-900 shadow-sm',
        className
      )}
      {...props}
    />
  )
);
Card.displayName = 'Card';

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex flex-col space-y-1.5 p-6', className)}
      {...props}
    />
  )
);
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-xl font-semibold leading-none tracking-tight text-gray-900 dark:text-gray-100', className)}
      {...props}
    />
  )
);
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('text-sm text-gray-500 dark:text-gray-400', className)}
      {...props}
    />
  )
);
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
  )
);
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('flex items-center p-6 pt-0', className)}
      {...props}
    />
  )
);
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
""")

    # ──────────────────────────────────────────────
    # Auth Files
    # ──────────────────────────────────────────────
    print("\n📁 Authentication Files")
    print("-" * 40)

    # 1. hooks/useAuth.ts
    create_file("hooks/useAuth.ts", """// خطاف المصادقة: يدير جلسة المستخدم والملف الشخصي والدور
// يشترك في تغييرات حالة المصادقة ويحدث المخزن تلقائياً
'use client';

import { useEffect, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import type { Profile, Role } from '@/types/user';
import type { AuthChangeEvent, Session } from '@supabase/supabase-js';

/**
 * واجهة القيم المرجعة من خطاف المصادقة
 */
interface UseAuthReturn {
  /** الملف الشخصي للمستخدم */
  user: Profile | null;
  /** دور المستخدم */
  role: Role;
  /** هل المستخدم مدير؟ */
  isAdmin: boolean;
  /** هل المستخدم مميز؟ */
  isPremium: boolean;
  /** هل المستخدم مجاني؟ */
  isFree: boolean;
  /** هل المستخدم مدير خارق؟ */
  isSuperAdmin: boolean;
  /** هل يتم تحميل البيانات؟ */
  isLoading: boolean;
  /** هل المستخدم محظور؟ */
  isBanned: boolean;
  /** تسجيل الدخول */
  signIn: (email: string, password: string) => Promise<{ error: string | null }>;
  /** إنشاء حساب */
  signUp: (email: string, password: string, displayName?: string) => Promise<{ error: string | null }>;
  /** تسجيل الخروج */
  signOut: () => Promise<void>;
  /** تحديث الملف الشخصي */
  refreshProfile: () => Promise<void>;
}

/**
 * خطاف المصادقة الرئيسي
 * يدير جلسة المستخدم والاشتراك في تغييرات الحالة
 */
export function useAuth(): UseAuthReturn {
  const router = useRouter();
  const supabase = createSupabaseBrowserClient();
  const subscriptionRef = useRef<{ unsubscribe: () => void } | null>(null);
  const initRef = useRef(false);

  const {
    user,
    role,
    isSuperAdmin,
    isLoading,
    isBanned,
    setUser,
    setSession,
    setLoading,
    clearAuth,
  } = useAuthStore();

  /**
   * جلب الملف الشخصي من قاعدة البيانات
   */
  const fetchProfile = useCallback(
    async (userId: string): Promise<Profile | null> => {
      try {
        const { data, error } = await supabase
          .from('profiles')
          .select('*')
          .eq('id', userId)
          .single();

        if (error) {
          if (process.env.NODE_ENV === 'development') {
            console.error('Error fetching profile:', error.message);
          }
          return null;
        }

        return data as Profile;
      } catch {
        return null;
      }
    },
    [supabase]
  );

  /**
   * تحديث الملف الشخصي
   */
  const refreshProfile = useCallback(async () => {
    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (session?.user) {
      const profile = await fetchProfile(session.user.id);
      if (profile) {
        setUser(profile);
      }
    }
  }, [supabase, fetchProfile, setUser]);

  /**
   * معالجة تغيير حالة المصادقة
   */
  const handleAuthChange = useCallback(
    async (event: AuthChangeEvent, session: Session | null) => {
      setSession(session);

      if (event === 'SIGNED_IN' && session?.user) {
        setLoading(true);
        const profile = await fetchProfile(session.user.id);
        if (profile) {
          if (profile.is_banned) {
            await supabase.auth.signOut();
            clearAuth();
            return;
          }
          setUser(profile);
        }
        setLoading(false);
      } else if (event === 'SIGNED_OUT') {
        clearAuth();
      } else if (event === 'TOKEN_REFRESHED' && session?.user) {
        const profile = await fetchProfile(session.user.id);
        if (profile) {
          setUser(profile);
        }
      }
    },
    [supabase, fetchProfile, setUser, setSession, setLoading, clearAuth]
  );

  /**
   * الاشتراك في تغييرات المصادقة عند التحميل
   */
  useEffect(() => {
    if (initRef.current) return;
    initRef.current = true;

    const initializeAuth = async () => {
      setLoading(true);

      try {
        const {
          data: { session },
        } = await supabase.auth.getSession();

        if (session?.user) {
          setSession(session);
          const profile = await fetchProfile(session.user.id);
          if (profile) {
            if (profile.is_banned) {
              await supabase.auth.signOut();
              clearAuth();
              return;
            }
            setUser(profile);
          }
        }
      } catch {
        clearAuth();
      } finally {
        setLoading(false);
      }

      const {
        data: { subscription },
      } = supabase.auth.onAuthStateChange(handleAuthChange);

      subscriptionRef.current = subscription;
    };

    initializeAuth();

    return () => {
      if (subscriptionRef.current) {
        subscriptionRef.current.unsubscribe();
        subscriptionRef.current = null;
      }
    };
  }, [supabase, fetchProfile, handleAuthChange, setUser, setSession, setLoading, clearAuth]);

  /**
   * تسجيل الدخول بالبريد وكلمة المرور
   */
  const signIn = useCallback(
    async (email: string, password: string): Promise<{ error: string | null }> => {
      try {
        setLoading(true);

        const { data, error } = await supabase.auth.signInWithPassword({
          email: email.trim().toLowerCase(),
          password,
        });

        if (error) {
          setLoading(false);

          if (error.message.includes('Invalid login credentials')) {
            return { error: 'error_invalid_credentials' };
          }
          if (error.message.includes('Email not confirmed')) {
            return { error: 'error_invalid_credentials' };
          }
          return { error: 'error_generic' };
        }

        if (data.session?.user) {
          const profile = await fetchProfile(data.session.user.id);
          if (profile?.is_banned) {
            await supabase.auth.signOut();
            clearAuth();
            return { error: 'error_banned' };
          }
          if (profile) {
            setUser(profile);
            setSession(data.session);
          }
        }

        setLoading(false);
        return { error: null };
      } catch {
        setLoading(false);
        return { error: 'error_network' };
      }
    },
    [supabase, fetchProfile, setUser, setSession, setLoading, clearAuth]
  );

  /**
   * إنشاء حساب جديد
   */
  const signUp = useCallback(
    async (
      email: string,
      password: string,
      displayName?: string
    ): Promise<{ error: string | null }> => {
      try {
        setLoading(true);

        const { data, error } = await supabase.auth.signUp({
          email: email.trim().toLowerCase(),
          password,
          options: {
            data: {
              display_name: displayName ?? email.split('@')[0],
            },
            emailRedirectTo: undefined,
          },
        });

        if (error) {
          setLoading(false);

          if (error.message.includes('already registered') || error.message.includes('already exists')) {
            return { error: 'error_email_exists' };
          }
          if (error.message.includes('weak_password') || error.message.includes('too short')) {
            return { error: 'error_weak_password' };
          }
          return { error: 'error_generic' };
        }

        if (data.session?.user) {
          const profile = await fetchProfile(data.session.user.id);
          if (profile) {
            setUser(profile);
            setSession(data.session);
          }
        } else if (data.user && !data.session) {
          const { data: signInData, error: signInError } = await supabase.auth.signInWithPassword({
            email: email.trim().toLowerCase(),
            password,
          });

          if (signInError) {
            setLoading(false);
            return { error: null };
          }

          if (signInData.session?.user) {
            const profile = await fetchProfile(signInData.session.user.id);
            if (profile) {
              setUser(profile);
              setSession(signInData.session);
            }
          }
        }

        setLoading(false);
        return { error: null };
      } catch {
        setLoading(false);
        return { error: 'error_network' };
      }
    },
    [supabase, fetchProfile, setUser, setSession, setLoading]
  );

  /**
   * تسجيل الخروج
   */
  const signOut = useCallback(async () => {
    try {
      await supabase.auth.signOut();
      clearAuth();
      router.push('/ar/login');
    } catch {
      clearAuth();
      router.push('/ar/login');
    }
  }, [supabase, clearAuth, router]);

  return {
    user,
    role,
    isAdmin: role === 'admin',
    isPremium: role === 'premium',
    isFree: role === 'free',
    isSuperAdmin,
    isLoading,
    isBanned,
    signIn,
    signUp,
    signOut,
    refreshProfile,
  };
}
""")

    # 2. components/auth/LoginForm.tsx
    create_file("components/auth/LoginForm.tsx", """// نموذج تسجيل الدخول: حقل البريد وكلمة المرور مع التحقق والأخطاء
'use client';

import { useState, useCallback, type FormEvent } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { Eye, EyeOff, LogIn, Mail, Lock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { useAuth } from '@/hooks/useAuth';
import { isValidEmail } from '@/utils/validators';
import { Link } from '@/i18n/navigation';

/**
 * مكون نموذج تسجيل الدخول
 */
export function LoginForm() {
  const t = useTranslations('auth');
  const locale = useLocale();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { signIn, isLoading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const redirectTo = searchParams.get('redirect');

  /**
   * معالجة إرسال النموذج
   */
  const handleSubmit = useCallback(
    async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setError('');

      if (!email.trim()) {
        setError(t('error_generic'));
        return;
      }

      if (!isValidEmail(email)) {
        setError(t('error_invalid_credentials'));
        return;
      }

      if (!password) {
        setError(t('error_generic'));
        return;
      }

      setIsSubmitting(true);

      try {
        const result = await signIn(email, password);

        if (result.error) {
          setError(t(result.error));
          setIsSubmitting(false);
          return;
        }

        const target = redirectTo ?? `/${locale}/chat`;
        router.push(target);
        router.refresh();
      } catch {
        setError(t('error_network'));
        setIsSubmitting(false);
      }
    },
    [email, password, signIn, router, locale, redirectTo, t]
  );

  const isFormLoading = isSubmitting || isLoading;

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* حقل البريد الإلكتروني */}
      <div className="space-y-2">
        <Label htmlFor="email" required>
          {t('email_label')}
        </Label>
        <div className="relative">
          <Mail className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="email"
            type="email"
            placeholder={t('email_placeholder')}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="ps-10"
            autoComplete="email"
            autoFocus
            disabled={isFormLoading}
            dir="ltr"
          />
        </div>
      </div>

      {/* حقل كلمة المرور */}
      <div className="space-y-2">
        <Label htmlFor="password" required>
          {t('password_label')}
        </Label>
        <div className="relative">
          <Lock className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            placeholder={t('password_placeholder')}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="ps-10 pe-10"
            autoComplete="current-password"
            disabled={isFormLoading}
            dir="ltr"
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute end-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
            tabIndex={-1}
          >
            {showPassword ? (
              <EyeOff className="h-4 w-4" />
            ) : (
              <Eye className="h-4 w-4" />
            )}
          </button>
        </div>
      </div>

      {/* رسالة الخطأ */}
      {error && <ErrorMessage message={error} dismissible onDismiss={() => setError('')} />}

      {/* زر تسجيل الدخول */}
      <Button
        type="submit"
        className="w-full"
        size="lg"
        isLoading={isFormLoading}
        disabled={isFormLoading || !email || !password}
      >
        {isFormLoading ? (
          t('logging_in')
        ) : (
          <>
            <LogIn className="h-4 w-4" />
            {t('login_button')}
          </>
        )}
      </Button>

      {/* رابط إنشاء حساب */}
      <p className="text-center text-sm text-gray-500 dark:text-gray-400">
        {t('no_account')}{' '}
        <Link
          href="/register"
          className="font-medium text-primary-500 hover:text-primary-600 transition-colors"
        >
          {t('register_button')}
        </Link>
      </p>
    </form>
  );
}
""")

    # 3. components/auth/RegisterForm.tsx
    create_file("components/auth/RegisterForm.tsx", """// نموذج إنشاء الحساب: حقول البريد وكلمة المرور مع مؤشر القوة
'use client';

import { useState, useCallback, useMemo, type FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { Eye, EyeOff, UserPlus, Mail, Lock, User } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { useAuth } from '@/hooks/useAuth';
import { isValidEmail, isValidPassword } from '@/utils/validators';
import { cn } from '@/utils/cn';
import { Link } from '@/i18n/navigation';

/**
 * مكون نموذج إنشاء الحساب
 */
export function RegisterForm() {
  const t = useTranslations('auth');
  const locale = useLocale();
  const router = useRouter();
  const { signUp, isLoading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * التحقق من قوة كلمة المرور
   */
  const passwordValidation = useMemo(() => {
    if (!password) return null;
    return isValidPassword(password);
  }, [password]);

  /**
   * لون مؤشر القوة
   */
  const strengthColor = useMemo(() => {
    if (!passwordValidation) return 'bg-gray-200 dark:bg-dark-700';

    switch (passwordValidation.strength) {
      case 'weak':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'strong':
        return 'bg-green-500';
      default:
        return 'bg-gray-200 dark:bg-dark-700';
    }
  }, [passwordValidation]);

  /**
   * نسبة مؤشر القوة
   */
  const strengthWidth = useMemo(() => {
    if (!passwordValidation) return '0%';

    switch (passwordValidation.strength) {
      case 'weak':
        return '33%';
      case 'medium':
        return '66%';
      case 'strong':
        return '100%';
      default:
        return '0%';
    }
  }, [passwordValidation]);

  /**
   * نص قوة كلمة المرور
   */
  const strengthText = useMemo(() => {
    if (!passwordValidation) return '';

    switch (passwordValidation.strength) {
      case 'weak':
        return t('password_strength_weak');
      case 'medium':
        return t('password_strength_medium');
      case 'strong':
        return t('password_strength_strong');
      default:
        return '';
    }
  }, [passwordValidation, t]);

  /**
   * التحقق من تطابق كلمات المرور
   */
  const passwordsMatch = useMemo(() => {
    if (!confirmPassword) return true;
    return password === confirmPassword;
  }, [password, confirmPassword]);

  /**
   * معالجة إرسال النموذج
   */
  const handleSubmit = useCallback(
    async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setError('');

      if (!isValidEmail(email)) {
        setError(t('error_invalid_credentials'));
        return;
      }

      if (!passwordValidation?.isValid) {
        setError(t('error_weak_password'));
        return;
      }

      if (password !== confirmPassword) {
        setError(t('passwords_not_match'));
        return;
      }

      setIsSubmitting(true);

      try {
        const result = await signUp(email, password, displayName || undefined);

        if (result.error) {
          setError(t(result.error));
          setIsSubmitting(false);
          return;
        }

        router.push(`/${locale}/chat`);
        router.refresh();
      } catch {
        setError(t('error_network'));
        setIsSubmitting(false);
      }
    },
    [email, password, confirmPassword, displayName, passwordValidation, signUp, router, locale, t]
  );

  const isFormLoading = isSubmitting || isLoading;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* حقل الاسم المعروض */}
      <div className="space-y-2">
        <Label htmlFor="displayName">{t('display_name_label')}</Label>
        <div className="relative">
          <User className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="displayName"
            type="text"
            placeholder={t('display_name_placeholder')}
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            className="ps-10"
            autoComplete="name"
            disabled={isFormLoading}
          />
        </div>
      </div>

      {/* حقل البريد الإلكتروني */}
      <div className="space-y-2">
        <Label htmlFor="register-email" required>
          {t('email_label')}
        </Label>
        <div className="relative">
          <Mail className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="register-email"
            type="email"
            placeholder={t('email_placeholder')}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="ps-10"
            autoComplete="email"
            autoFocus
            disabled={isFormLoading}
            dir="ltr"
          />
        </div>
      </div>

      {/* حقل كلمة المرور */}
      <div className="space-y-2">
        <Label htmlFor="register-password" required>
          {t('password_label')}
        </Label>
        <div className="relative">
          <Lock className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="register-password"
            type={showPassword ? 'text' : 'password'}
            placeholder={t('password_placeholder')}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="ps-10 pe-10"
            autoComplete="new-password"
            disabled={isFormLoading}
            dir="ltr"
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute end-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
            tabIndex={-1}
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>

        {/* مؤشر قوة كلمة المرور */}
        {password && (
          <div className="space-y-1.5">
            <div className="h-1.5 w-full rounded-full bg-gray-200 dark:bg-dark-700 overflow-hidden">
              <div
                className={cn('h-full rounded-full transition-all duration-300', strengthColor)}
                style={{ width: strengthWidth }}
              />
            </div>
            <p
              className={cn('text-xs', {
                'text-red-500': passwordValidation?.strength === 'weak',
                'text-yellow-500': passwordValidation?.strength === 'medium',
                'text-green-500': passwordValidation?.strength === 'strong',
              })}
            >
              {strengthText}
            </p>
          </div>
        )}
      </div>

      {/* حقل تأكيد كلمة المرور */}
      <div className="space-y-2">
        <Label htmlFor="confirm-password" required>
          {t('confirm_password_label')}
        </Label>
        <div className="relative">
          <Lock className="absolute start-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            id="confirm-password"
            type={showConfirmPassword ? 'text' : 'password'}
            placeholder={t('confirm_password_placeholder')}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={cn('ps-10 pe-10', !passwordsMatch && confirmPassword && 'border-red-500')}
            autoComplete="new-password"
            disabled={isFormLoading}
            dir="ltr"
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute end-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            tabIndex={-1}
          >
            {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        {!passwordsMatch && confirmPassword && (
          <p className="text-xs text-red-500">{t('passwords_not_match')}</p>
        )}
      </div>

      {/* رسالة الخطأ */}
      {error && <ErrorMessage message={error} dismissible onDismiss={() => setError('')} />}

      {/* زر إنشاء الحساب */}
      <Button
        type="submit"
        className="w-full"
        size="lg"
        isLoading={isFormLoading}
        disabled={
          isFormLoading ||
          !email ||
          !password ||
          !confirmPassword ||
          !passwordsMatch ||
          !passwordValidation?.isValid
        }
      >
        {isFormLoading ? (
          t('registering')
        ) : (
          <>
            <UserPlus className="h-4 w-4" />
            {t('register_button')}
          </>
        )}
      </Button>

      {/* رابط تسجيل الدخول */}
      <p className="text-center text-sm text-gray-500 dark:text-gray-400">
        {t('have_account')}{' '}
        <Link
          href="/login"
          className="font-medium text-primary-500 hover:text-primary-600 transition-colors"
        >
          {t('login_button')}
        </Link>
      </p>
    </form>
  );
}
""")

    # 4. components/auth/RouteGuard.tsx
    create_file("components/auth/RouteGuard.tsx", """// حارس المسار: يحمي الصفحات ويتحقق من المصادقة والصلاحيات
'use client';

import { useEffect, type ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useLocale } from 'next-intl';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { useAuth } from '@/hooks/useAuth';

/**
 * خصائص حارس المسار
 */
interface RouteGuardProps {
  /** المحتوى المحمي */
  children: ReactNode;
  /** يتطلب دور مدير */
  requireAdmin?: boolean;
  /** يتطلب دور مميز أو أعلى */
  requirePremium?: boolean;
}

/**
 * مكون حارس المسار
 * يتحقق من المصادقة والصلاحيات قبل عرض المحتوى
 */
export function RouteGuard({
  children,
  requireAdmin = false,
  requirePremium = false,
}: RouteGuardProps) {
  const { user, isLoading, isBanned, isAdmin, isPremium, role } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();

  useEffect(() => {
    if (isLoading) return;

    // المستخدم غير مسجل
    if (!user) {
      const loginPath = `/${locale}/login`;
      const redirect = pathname !== loginPath ? `?redirect=${encodeURIComponent(pathname)}` : '';
      router.replace(`${loginPath}${redirect}`);
      return;
    }

    // المستخدم محظور
    if (isBanned) {
      router.replace(`/${locale}/login`);
      return;
    }

    // يتطلب صلاحية مدير
    if (requireAdmin && !isAdmin) {
      router.replace(`/${locale}/chat`);
      return;
    }

    // يتطلب صلاحية مميزة
    if (requirePremium && role === 'free') {
      router.replace(`/${locale}/chat`);
      return;
    }
  }, [user, isLoading, isBanned, isAdmin, isPremium, role, requireAdmin, requirePremium, router, pathname, locale]);

  // حالة التحميل
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white dark:bg-dark-950">
        <LoadingSpinner size="lg" text="Loading..." />
      </div>
    );
  }

  // المستخدم غير مسجل
  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-white dark:bg-dark-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // المستخدم محظور
  if (isBanned) {
    return null;
  }

  // يتطلب مدير لكن المستخدم ليس مديراً
  if (requireAdmin && !isAdmin) {
    return null;
  }

  // يتطلب مميز لكن المستخدم مجاني
  if (requirePremium && role === 'free') {
    return null;
  }

  return <>{children}</>;
}
""")

    # 5. app/[locale]/login/page.tsx
    create_file("app/[locale]/login/page.tsx", """// صفحة تسجيل الدخول: نموذج الدخول مع الشعار والتوجيه
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Logo } from '@/components/common/Logo';
import { LoginForm } from '@/components/auth/LoginForm';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';

/**
 * صفحة تسجيل الدخول
 */
export default function LoginPage() {
  const t = useTranslations('auth');
  const locale = useLocale();
  const router = useRouter();
  const { user, isLoading } = useAuth();

  // إعادة التوجيه إذا كان المستخدم مسجلاً بالفعل
  useEffect(() => {
    if (!isLoading && user) {
      router.replace(`/${locale}/chat`);
    }
  }, [user, isLoading, router, locale]);

  // حالة التحميل
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // المستخدم مسجل بالفعل
  if (user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 p-4">
      {/* خلفية زخرفية */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -end-40 h-80 w-80 rounded-full bg-primary-500/10 blur-3xl" />
        <div className="absolute -bottom-40 -start-40 h-80 w-80 rounded-full bg-secondary-500/10 blur-3xl" />
      </div>

      <Card className="relative w-full max-w-md border-dark-700 bg-dark-900/95 backdrop-blur-xl shadow-2xl">
        <CardHeader className="items-center space-y-4 pb-2">
          <Logo size="lg" />
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-100">
              {t('login_title')}
            </h1>
          </div>
        </CardHeader>
        <CardContent className="pt-4">
          <LoginForm />
        </CardContent>
      </Card>
    </div>
  );
}
""")

    # 6. app/[locale]/register/page.tsx
    create_file("app/[locale]/register/page.tsx", """// صفحة إنشاء الحساب: نموذج التسجيل مع الشعار والتوجيه
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Logo } from '@/components/common/Logo';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';

/**
 * صفحة إنشاء الحساب
 */
export default function RegisterPage() {
  const t = useTranslations('auth');
  const locale = useLocale();
  const router = useRouter();
  const { user, isLoading } = useAuth();

  // إعادة التوجيه إذا كان المستخدم مسجلاً بالفعل
  useEffect(() => {
    if (!isLoading && user) {
      router.replace(`/${locale}/chat`);
    }
  }, [user, isLoading, router, locale]);

  // حالة التحميل
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // المستخدم مسجل بالفعل
  if (user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 p-4">
      {/* خلفية زخرفية */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -end-40 h-80 w-80 rounded-full bg-primary-500/10 blur-3xl" />
        <div className="absolute -bottom-40 -start-40 h-80 w-80 rounded-full bg-accent-500/10 blur-3xl" />
      </div>

      <Card className="relative w-full max-w-md border-dark-700 bg-dark-900/95 backdrop-blur-xl shadow-2xl">
        <CardHeader className="items-center space-y-4 pb-2">
          <Logo size="lg" />
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-100">
              {t('register_title')}
            </h1>
          </div>
        </CardHeader>
        <CardContent className="pt-4">
          <RegisterForm />
        </CardContent>
      </Card>
    </div>
  );
}
""")

    # 7. app/[locale]/invite/[code]/page.tsx
    create_file("app/[locale]/invite/[code]/page.tsx", """// صفحة كود الدعوة: عرض الكود وتفعيله للحصول على الحساب المميز
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslations, useLocale } from 'next-intl';
import { Gift, CheckCircle, XCircle, Loader2, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Logo } from '@/components/common/Logo';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { RouteGuard } from '@/components/auth/RouteGuard';
import { useAuth } from '@/hooks/useAuth';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { isValidInviteCode } from '@/utils/validators';

/**
 * خصائص صفحة كود الدعوة
 */
interface InviteCodePageProps {
  params: { code: string; locale: string };
}

/**
 * معلومات كود الدعوة
 */
interface InviteCodeInfo {
  id: string;
  code: string;
  maxUses: number;
  currentUses: number;
  premiumDurationDays: number | null;
  isActive: boolean;
  expiresAt: string | null;
}

/**
 * صفحة كود الدعوة
 */
export default function InviteCodePage({ params }: InviteCodePageProps) {
  return (
    <RouteGuard>
      <InviteCodeContent code={params.code} />
    </RouteGuard>
  );
}

/**
 * محتوى صفحة كود الدعوة
 */
function InviteCodeContent({ code }: { code: string }) {
  const t = useTranslations('settings');
  const tCommon = useTranslations('common');
  const locale = useLocale();
  const router = useRouter();
  const { user, refreshProfile, role } = useAuth();
  const supabase = createSupabaseBrowserClient();

  const [codeInfo, setCodeInfo] = useState<InviteCodeInfo | null>(null);
  const [isLoadingCode, setIsLoadingCode] = useState(true);
  const [isActivating, setIsActivating] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  /**
   * جلب معلومات الكود
   */
  const fetchCodeInfo = useCallback(async () => {
    setIsLoadingCode(true);
    setError('');

    try {
      if (!isValidInviteCode(code)) {
        setError(t('code_invalid'));
        setIsLoadingCode(false);
        return;
      }

      const response = await fetch(`/api/admin/invite-codes?code=${encodeURIComponent(code)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({})) as Record<string, string>;
        setError(data.error ?? t('code_invalid'));
        setIsLoadingCode(false);
        return;
      }

      const data = await response.json() as InviteCodeInfo;
      setCodeInfo(data);
    } catch {
      setError(t('code_invalid'));
    } finally {
      setIsLoadingCode(false);
    }
  }, [code, t]);

  useEffect(() => {
    fetchCodeInfo();

    return () => {
      // cleanup
    };
  }, [fetchCodeInfo]);

  /**
   * تفعيل الكود
   */
  const activateCode = useCallback(async () => {
    if (!user || !codeInfo) return;

    setIsActivating(true);
    setError('');

    try {
      // التحقق من أن الكود لا يزال نشطاً
      if (!codeInfo.isActive) {
        setError(t('code_invalid'));
        setIsActivating(false);
        return;
      }

      // التحقق من انتهاء الصلاحية
      if (codeInfo.expiresAt && new Date(codeInfo.expiresAt) < new Date()) {
        setError(t('code_expired'));
        setIsActivating(false);
        return;
      }

      // التحقق من الحد الأقصى للاستخدام
      if (codeInfo.currentUses >= codeInfo.maxUses) {
        setError(t('code_used'));
        setIsActivating(false);
        return;
      }

      // التحقق من الاستخدام السابق
      const { data: existingUse } = await supabase
        .from('invite_code_uses')
        .select('id')
        .eq('invite_code_id', codeInfo.id)
        .eq('user_id', user.id)
        .single();

      if (existingUse) {
        setError(t('code_already_used'));
        setIsActivating(false);
        return;
      }

      // حساب تاريخ انتهاء الاشتراك المميز
      let premiumExpiresAt: string | null = null;
      if (codeInfo.premiumDurationDays) {
        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + codeInfo.premiumDurationDays);
        premiumExpiresAt = expiryDate.toISOString();
      }

      // تحديث الملف الشخصي
      const updateData: Record<string, unknown> = {
        role: 'premium' as const,
        updated_at: new Date().toISOString(),
      };

      if (premiumExpiresAt) {
        updateData.premium_expires_at = premiumExpiresAt;
      }

      const { error: profileError } = await supabase
        .from('profiles')
        .update(updateData)
        .eq('id', user.id);

      if (profileError) {
        setError(t('code_invalid'));
        setIsActivating(false);
        return;
      }

      // تسجيل استخدام الكود
      const { error: useError } = await supabase
        .from('invite_code_uses')
        .insert({
          invite_code_id: codeInfo.id,
          user_id: user.id,
        });

      if (useError) {
        // الاستخدام مسجل بالفعل أو خطأ آخر - لكن الملف الشخصي تم تحديثه
        if (process.env.NODE_ENV === 'development') {
          console.error('Error recording invite code use:', useError.message);
        }
      }

      // تحديث عداد الاستخدام
      await supabase
        .from('invite_codes')
        .update({ current_uses: codeInfo.currentUses + 1 })
        .eq('id', codeInfo.id);

      // إنشاء إشعار
      await supabase.from('notifications').insert({
        type: 'invite_code_used',
        title: 'استخدام كود دعوة',
        message: `تم استخدام كود الدعوة ${codeInfo.code} بواسطة ${user.email}`,
        priority: 'info',
        related_user_id: user.id,
        metadata: {
          code: codeInfo.code,
          user_email: user.email,
          premium_duration_days: codeInfo.premiumDurationDays,
        },
      });

      setSuccess(true);
      await refreshProfile();

      // الانتقال لصفحة الدردشة بعد ثانيتين
      setTimeout(() => {
        router.push(`/${locale}/chat`);
      }, 2000);
    } catch {
      setError(t('code_invalid'));
    } finally {
      setIsActivating(false);
    }
  }, [user, codeInfo, supabase, refreshProfile, router, locale, t]);

  // المستخدم بالفعل مميز
  if (role === 'premium' || role === 'admin') {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 p-4">
        <Card className="w-full max-w-md border-dark-700 bg-dark-900/95 backdrop-blur-xl">
          <CardHeader className="items-center text-center">
            <Sparkles className="h-12 w-12 text-primary-500 mb-2" />
            <CardTitle className="text-gray-100">
              {role === 'admin' ? tCommon('admin') : tCommon('premium')}
            </CardTitle>
            <CardDescription>
              {role === 'admin'
                ? 'أنت مدير بالفعل ولديك جميع الصلاحيات'
                : 'لديك حساب مميز بالفعل'}
            </CardDescription>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Button onClick={() => router.push(`/${locale}/chat`)}>
              {tCommon('back')}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // حالة التحميل
  if (isLoadingCode) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
        <LoadingSpinner size="lg" text={tCommon('loading')} />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950 p-4">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -end-40 h-80 w-80 rounded-full bg-primary-500/10 blur-3xl" />
        <div className="absolute -bottom-40 -start-40 h-80 w-80 rounded-full bg-accent-500/10 blur-3xl" />
      </div>

      <Card className="relative w-full max-w-md border-dark-700 bg-dark-900/95 backdrop-blur-xl shadow-2xl">
        <CardHeader className="items-center text-center space-y-4">
          <Logo size="lg" />

          {success ? (
            <>
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500/20">
                <CheckCircle className="h-10 w-10 text-green-500" />
              </div>
              <CardTitle className="text-green-400">
                {t('code_success')}
              </CardTitle>
              <CardDescription>
                {codeInfo?.premiumDurationDays
                  ? `مدة الاشتراك: ${codeInfo.premiumDurationDays} يوم`
                  : tCommon('permanent')}
              </CardDescription>
            </>
          ) : error && !codeInfo ? (
            <>
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-500/20">
                <XCircle className="h-10 w-10 text-red-500" />
              </div>
              <CardTitle className="text-red-400">{error}</CardTitle>
            </>
          ) : (
            <>
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-500/20">
                <Gift className="h-10 w-10 text-primary-500" />
              </div>
              <CardTitle className="text-gray-100">{t('invite_code_label')}</CardTitle>
              <CardDescription>
                {codeInfo?.premiumDurationDays
                  ? `الترقية للحساب المميز لمدة ${codeInfo.premiumDurationDays} يوم`
                  : 'الترقية للحساب المميز بشكل دائم'}
              </CardDescription>
            </>
          )}
        </CardHeader>

        <CardContent className="space-y-4">
          {/* عرض الكود */}
          {codeInfo && !success && (
            <>
              <div className="flex items-center justify-center rounded-lg bg-dark-800 border border-dark-600 p-4">
                <code className="text-xl font-mono font-bold text-primary-400 tracking-wider">
                  {code}
                </code>
              </div>

              {/* معلومات الكود */}
              <div className="space-y-2 text-sm text-gray-400">
                {codeInfo.premiumDurationDays && (
                  <div className="flex items-center justify-between">
                    <span>مدة الاشتراك:</span>
                    <span className="text-primary-400 font-medium">
                      {codeInfo.premiumDurationDays} يوم
                    </span>
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <span>الاستخدامات:</span>
                  <span className="text-gray-300">
                    {codeInfo.currentUses} / {codeInfo.maxUses}
                  </span>
                </div>
              </div>

              {/* رسالة الخطأ */}
              {error && (
                <ErrorMessage
                  message={error}
                  dismissible
                  onDismiss={() => setError('')}
                />
              )}

              {/* زر التفعيل */}
              <Button
                onClick={activateCode}
                className="w-full"
                size="lg"
                isLoading={isActivating}
                disabled={isActivating}
              >
                {isActivating ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    جاري التفعيل...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    {t('activate_code')}
                  </>
                )}
              </Button>
            </>
          )}

          {/* حالة عدم وجود الكود أو خطأ */}
          {!codeInfo && error && (
            <div className="flex justify-center">
              <Button
                variant="outline"
                onClick={() => router.push(`/${locale}/chat`)}
              >
                {tCommon('back')}
              </Button>
            </div>
          )}

          {/* بعد النجاح */}
          {success && (
            <div className="flex justify-center">
              <Button onClick={() => router.push(`/${locale}/chat`)}>
                ابدأ الاستخدام
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
""")

    # 8. app/api/auth/callback/route.ts
    create_file("app/api/auth/callback/route.ts", """// مسار API للمصادقة: معالجة رد الاستدعاء من Supabase Auth
// يُستخدم لتبادل رمز المصادقة للحصول على جلسة
import { NextResponse, type NextRequest } from 'next/server';
import { createSupabaseServerClientFromRequest } from '@/lib/supabase-server';

/**
 * معالجة طلب GET لرد الاستدعاء
 * يتبادل رمز المصادقة مقابل جلسة
 */
export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');
  const redirectTo = requestUrl.searchParams.get('redirect') ?? '/ar/chat';

  if (code) {
    try {
      const supabase = createSupabaseServerClientFromRequest(request);
      const { error } = await supabase.auth.exchangeCodeForSession(code);

      if (error) {
        if (process.env.NODE_ENV === 'development') {
          console.error('Auth callback error:', error.message);
        }
        return NextResponse.redirect(
          new URL('/ar/login?error=auth_callback_failed', requestUrl.origin)
        );
      }
    } catch {
      return NextResponse.redirect(
        new URL('/ar/login?error=auth_callback_error', requestUrl.origin)
      );
    }
  }

  return NextResponse.redirect(new URL(redirectTo, requestUrl.origin));
}
""")

    # ──────────────────────────────────────────────
    # API route for invite code validation (needed by invite page)
    # ──────────────────────────────────────────────
    create_file("app/api/admin/invite-codes/route.ts", """// مسار API لأكواد الدعوة: جلب معلومات الكود والتحقق من صلاحيته
import { NextResponse, type NextRequest } from 'next/server';
import { createSupabaseServerClient } from '@/lib/supabase-server';
import { createSupabaseAdminClient } from '@/lib/supabase-admin';

/**
 * GET - جلب معلومات كود الدعوة (للمستخدمين العاديين عبر query param)
 * أو جلب جميع الأكواد (للمديرين)
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const code = searchParams.get('code');

    // إذا تم تمرير كود محدد - يمكن لأي مستخدم مصادق
    if (code) {
      const supabase = createSupabaseServerClient();

      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        return NextResponse.json(
          { error: 'غير مصرح' },
          { status: 401 }
        );
      }

      // استخدام العميل الإداري لجلب الكود (لأن RLS يمنع المستخدمين العاديين)
      const adminClient = createSupabaseAdminClient();

      const { data: inviteCode, error } = await adminClient
        .from('invite_codes')
        .select('*')
        .eq('code', code)
        .eq('is_active', true)
        .single();

      if (error || !inviteCode) {
        return NextResponse.json(
          { error: 'كود غير صالح' },
          { status: 404 }
        );
      }

      // التحقق من انتهاء الصلاحية
      if (inviteCode.expires_at && new Date(inviteCode.expires_at) < new Date()) {
        return NextResponse.json(
          { error: 'كود منتهي الصلاحية' },
          { status: 410 }
        );
      }

      // التحقق من الحد الأقصى
      if (inviteCode.current_uses >= inviteCode.max_uses) {
        return NextResponse.json(
          { error: 'كود مستخدم بالكامل' },
          { status: 410 }
        );
      }

      return NextResponse.json({
        id: inviteCode.id,
        code: inviteCode.code,
        maxUses: inviteCode.max_uses,
        currentUses: inviteCode.current_uses,
        premiumDurationDays: inviteCode.premium_duration_days,
        isActive: inviteCode.is_active,
        expiresAt: inviteCode.expires_at,
      });
    }

    // جلب جميع الأكواد - للمديرين فقط
    const supabase = createSupabaseServerClient();

    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 401 });
    }

    // التحقق من أن المستخدم مدير
    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', session.user.id)
      .single();

    if (!profile || profile.role !== 'admin') {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 403 });
    }

    const adminClient = createSupabaseAdminClient();

    const { data: codes, error: codesError } = await adminClient
      .from('invite_codes')
      .select('*')
      .order('created_at', { ascending: false });

    if (codesError) {
      return NextResponse.json(
        { error: 'خطأ في جلب الأكواد' },
        { status: 500 }
      );
    }

    return NextResponse.json(codes);
  } catch {
    return NextResponse.json(
      { error: 'خطأ في الخادم' },
      { status: 500 }
    );
  }
}

/**
 * POST - إنشاء كود دعوة جديد (للمديرين فقط)
 */
export async function POST(request: NextRequest) {
  try {
    const supabase = createSupabaseServerClient();

    const {
      data: { session },
    } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 401 });
    }

    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', session.user.id)
      .single();

    if (!profile || profile.role !== 'admin') {
      return NextResponse.json({ error: 'غير مصرح' }, { status: 403 });
    }

    const body = await request.json() as {
      code?: string;
      max_uses?: number;
      premium_duration_days?: number;
      expires_at?: string;
    };

    const adminClient = createSupabaseAdminClient();

    const { data: newCode, error: createError } = await adminClient
      .from('invite_codes')
      .insert({
        code: body.code ?? generateCode(),
        created_by: session.user.id,
        max_uses: body.max_uses ?? 1,
        premium_duration_days: body.premium_duration_days ?? null,
        is_active: true,
        expires_at: body.expires_at ?? null,
      })
      .select()
      .single();

    if (createError) {
      if (createError.message.includes('unique') || createError.message.includes('duplicate')) {
        return NextResponse.json(
          { error: 'الكود موجود بالفعل' },
          { status: 409 }
        );
      }
      return NextResponse.json(
        { error: 'خطأ في إنشاء الكود' },
        { status: 500 }
      );
    }

    return NextResponse.json(newCode, { status: 201 });
  } catch {
    return NextResponse.json(
      { error: 'خطأ في الخادم' },
      { status: 500 }
    );
  }
}

/**
 * توليد كود عشوائي
 */
function generateCode(length: number = 8): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
  let result = '';
  const array = new Uint8Array(length);
  crypto.getRandomValues(array);
  for (let i = 0; i < length; i++) {
    const idx = array[i];
    if (idx !== undefined) {
      result += chars[idx % chars.length];
    }
  }
  return result;
}
""")

    # ──────────────────────────────────────────────
    # Toast component (referenced in many places)
    # ──────────────────────────────────────────────
    create_file("components/ui/toast.tsx", """// مكون الإشعارات المنبثقة (Toast): لعرض رسائل النجاح والخطأ
'use client';

import { useState, useEffect, useCallback, createContext, useContext, type ReactNode } from 'react';
import { cn } from '@/utils/cn';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

/**
 * نوع الإشعار المنبثق
 */
type ToastType = 'success' | 'error' | 'warning' | 'info';

/**
 * بيانات الإشعار المنبثق
 */
interface ToastData {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

/**
 * سياق الإشعارات المنبثقة
 */
interface ToastContextType {
  toasts: ToastData[];
  addToast: (type: ToastType, message: string, duration?: number) => void;
  removeToast: (id: string) => void;
  success: (message: string) => void;
  error: (message: string) => void;
  warning: (message: string) => void;
  info: (message: string) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

/**
 * مزود الإشعارات المنبثقة
 */
export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastData[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const addToast = useCallback(
    (type: ToastType, message: string, duration: number = 5000) => {
      const id = `toast-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      const newToast: ToastData = { id, type, message, duration };

      setToasts((prev) => [...prev, newToast]);

      if (duration > 0) {
        setTimeout(() => {
          removeToast(id);
        }, duration);
      }
    },
    [removeToast]
  );

  const contextValue: ToastContextType = {
    toasts,
    addToast,
    removeToast,
    success: (message: string) => addToast('success', message),
    error: (message: string) => addToast('error', message),
    warning: (message: string) => addToast('warning', message),
    info: (message: string) => addToast('info', message),
  };

  return (
    <ToastContext.Provider value={contextValue}>
      {children}
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </ToastContext.Provider>
  );
}

/**
 * خطاف استخدام الإشعارات المنبثقة
 */
export function useToast(): ToastContextType {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

/**
 * حاوية الإشعارات المنبثقة
 */
function ToastContainer({
  toasts,
  removeToast,
}: {
  toasts: ToastData[];
  removeToast: (id: string) => void;
}) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 start-4 z-toast flex flex-col gap-2 max-w-sm w-full">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={removeToast} />
      ))}
    </div>
  );
}

/**
 * عنصر الإشعار المنبثق
 */
function ToastItem({
  toast,
  onRemove,
}: {
  toast: ToastData;
  onRemove: (id: string) => void;
}) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), 10);
    return () => clearTimeout(timer);
  }, []);

  const icons = {
    success: <CheckCircle className="h-5 w-5 text-green-400" />,
    error: <AlertCircle className="h-5 w-5 text-red-400" />,
    warning: <AlertTriangle className="h-5 w-5 text-yellow-400" />,
    info: <Info className="h-5 w-5 text-blue-400" />,
  };

  const borderColors = {
    success: 'border-green-500/30',
    error: 'border-red-500/30',
    warning: 'border-yellow-500/30',
    info: 'border-blue-500/30',
  };

  return (
    <div
      className={cn(
        'flex items-start gap-3 rounded-lg border bg-dark-900/95 backdrop-blur-xl p-3 shadow-lg transition-all duration-300',
        borderColors[toast.type],
        isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'
      )}
    >
      <div className="shrink-0 mt-0.5">{icons[toast.type]}</div>
      <p className="flex-1 text-sm text-gray-200">{toast.message}</p>
      <button
        onClick={() => onRemove(toast.id)}
        className="shrink-0 rounded p-0.5 text-gray-400 hover:text-gray-200 transition-colors"
        aria-label="Close notification"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}
""")

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 2 SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print()
    print("  PREREQUISITES (UI Components):")
    print("    • components/common/LoadingSpinner.tsx")
    print("    • components/common/Logo.tsx")
    print("    • components/common/ErrorMessage.tsx")
    print("    • components/ui/button.tsx     (Shadcn Button with variants)")
    print("    • components/ui/input.tsx      (Shadcn Input with error)")
    print("    • components/ui/label.tsx      (Shadcn Label with required)")
    print("    • components/ui/card.tsx       (Shadcn Card with sections)")
    print("    • components/ui/toast.tsx      (Toast system with provider)")
    print()
    print("  CORE AUTH FILES:")
    print("    1. hooks/useAuth.ts                  (Auth hook - signIn/signUp/signOut)")
    print("    2. components/auth/LoginForm.tsx      (Login form with validation)")
    print("    3. components/auth/RegisterForm.tsx   (Register form with strength)")
    print("    4. components/auth/RouteGuard.tsx     (Route protection component)")
    print("    5. app/[locale]/login/page.tsx        (Login page)")
    print("    6. app/[locale]/register/page.tsx     (Register page)")
    print("    7. app/[locale]/invite/[code]/page.tsx (Invite code activation)")
    print("    8. app/api/auth/callback/route.ts     (Auth callback handler)")
    print("    +  app/api/admin/invite-codes/route.ts (Invite codes API)")
    print()
    print("📝 NOTES:")
    print("  - useAuth subscribes to onAuthStateChange with proper cleanup")
    print("  - Login/Register forms use i18n for ALL text via useTranslations")
    print("  - Password strength indicator: red(weak) → yellow(medium) → green(strong)")
    print("  - RouteGuard handles: not-auth → login, banned → login, non-admin → chat")
    print("  - Invite code page validates: exists, active, not expired, not maxed, not reused")
    print("  - On invite success: upgrades role, sets expiry, records use, sends notification")
    print("  - All forms have RTL/LTR support with start/end positioning")
    print("  - Toast provider system for success/error notifications")
    print("  - All inputs have proper autocomplete attributes")
    print("  - All icon buttons have aria-label attributes")
    print("  - No 'any' type used - TypeScript strict mode throughout")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 3A: Chat core (API route, AI providers, encryption)")
    print("  Phase 3B: Chat UI (sidebar, header, message components)")
    print("  Phase 3C: Chat features (streaming, slash commands, rate limiting)")
    print("  Phase 4:  API Keys management")
    print("  Phase 5A: Features (personas, folders)")
    print("  Phase 5B: Features (favorites, export, onboarding)")
    print("  Phase 6A: Admin panel (layout, dashboard, users)")
    print("  Phase 6B: Admin panel (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (worker proxy, telegram, polish)")
    print()
    print("✅ Phase 2 Complete! Ready for Phase 3A.")


if __name__ == "__main__":
    main()
